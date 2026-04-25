#!/usr/bin/env python3
"""skillmanager — symlink manager for LLM skill directories

Every skill lives at skills/<name>/ (single kebab-case directory name).
LLM visibility is controlled by metadata.status in that skill's SKILL.md:
  active          → symlinks in each configured ~/.*/skills/
  staging         → symlinks in ~/.*/skills-staging/ only
  review|deactivated|decommissioned → no LLM symlinks
Omitted status defaults to active. Run "skillmanager audit" after editing status.

Usage: skillmanager <command> [args]
Run 'skillmanager help' for full usage.
"""

import os
import sys
import re
import shutil
import hashlib
import subprocess
import datetime
import platform
from pathlib import Path

IS_WINDOWS = sys.platform == "win32"

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"

if _supports_color():
    BOLD   = "\033[1m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    RED    = "\033[31m"
    CYAN   = "\033[36m"
    RESET  = "\033[0m"
else:
    BOLD = GREEN = YELLOW = RED = CYAN = RESET = ""

_ERR_COLOR = "\033[31m" if _supports_color() else ""
_RST_COLOR = "\033[0m"  if _supports_color() else ""


def die(msg: str) -> None:
    print(f"{RED}[ERROR]{RESET} {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET}  {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET}  {msg}")


def ok(msg: str) -> None:
    print(f"{GREEN}[OK]{RESET}    {msg}")


# ---------------------------------------------------------------------------
# YAML subset parser  (covers the config.yaml structure only)
# ---------------------------------------------------------------------------

def _parse_yaml(path: Path) -> dict:
    """Parse the limited YAML subset used in config.yaml.
    Handles: scalar key-value pairs, dict sections, list-of-dict sections.
    No external dependencies required.
    """
    config: dict = {}
    if not path.exists():
        return config

    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        i += 1

        if not stripped or stripped.startswith("#"):
            continue
        if indent != 0:
            continue  # nested lines handled in the peek loop below

        if ":" not in stripped:
            continue

        key, _, raw_val = stripped.partition(":")
        key = key.strip()
        val = raw_val.strip().strip("\"'")

        if val:
            config[key] = val
            continue

        # Peek ahead: determine if child content is a list or a dict
        children: dict = {}
        child_list: list = []
        is_list = False
        current_item: dict | None = None

        while i < len(lines):
            child_line = lines[i]
            child_stripped = child_line.strip()
            child_indent = len(child_line) - len(child_line.lstrip())

            if not child_stripped or child_stripped.startswith("#"):
                i += 1
                continue
            if child_indent == 0:
                break  # back at top level

            if child_stripped.startswith("- "):
                is_list = True
                rest = child_stripped[2:].strip()
                current_item = {}
                child_list.append(current_item)
                if ":" in rest:
                    k, _, v = rest.partition(":")
                    current_item[k.strip()] = v.strip().strip("\"'")
            elif child_stripped.startswith("-"):
                is_list = True
                current_item = {}
                child_list.append(current_item)
            else:
                if is_list and current_item is not None:
                    if ":" in child_stripped:
                        k, _, v = child_stripped.partition(":")
                        current_item[k.strip()] = v.strip().strip("\"'")
                else:
                    if ":" in child_stripped:
                        k, _, v = child_stripped.partition(":")
                        children[k.strip()] = v.strip().strip("\"'")

            i += 1

        config[key] = child_list if is_list else children

    return config


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_HOME = Path.home()

def _expand(p: str) -> Path:
    return Path(p.replace("~", str(_HOME)))


def _get_config_file() -> Path:
    skillmanager_dir = os.environ.get("SKILLMANAGER_DIR", "")
    if skillmanager_dir:
        return _expand(skillmanager_dir) / "config.yaml"
    return _HOME / ".skillmanager" / "config.yaml"


def _load_config() -> dict:
    return _parse_yaml(_get_config_file())


def _get_skillmanager_dir() -> Path:
    env_val = os.environ.get("SKILLMANAGER_DIR", "")
    if env_val:
        return _expand(env_val)
    cfg = _load_config()
    install_dir = cfg.get("install_dir", "")
    if install_dir:
        return _expand(install_dir)
    return _HOME / ".skillmanager"


def _get_skills_dir() -> Path:
    return _get_skillmanager_dir() / "skills"


def _get_llm_skill_dirs() -> list[Path]:
    """Return configured LLM production skill dirs from config.yaml."""
    cfg = _load_config()
    targets = cfg.get("llm_targets", [])
    if isinstance(targets, list):
        dirs = []
        for t in targets:
            if isinstance(t, dict) and "skills_dir" in t:
                d = _expand(t["skills_dir"])
                if d.is_dir():
                    dirs.append(d)
        if dirs:
            return dirs

    # Fallback to defaults when config absent or empty
    fallbacks = []
    for default in [_HOME / ".claude" / "skills", _HOME / ".gemini" / "skills"]:
        if default.is_dir():
            fallbacks.append(default)
    return fallbacks


def _get_staging_dirs() -> list[Path]:
    """Return staging dirs derived from production dirs."""
    return [Path(str(d).replace("skills", "skills-staging")) for d in _get_llm_skill_dirs()]


# ---------------------------------------------------------------------------
# Symlink helpers (platform-aware)
# ---------------------------------------------------------------------------

def _safe_symlink(src: Path, dst: Path) -> bool:
    """Create dst → src symlink. Returns True on success."""
    try:
        if dst.is_symlink():
            dst.unlink()
        os.symlink(src, dst)
        return True
    except OSError as exc:
        if IS_WINDOWS and hasattr(exc, "winerror") and exc.winerror == 1314:
            warn(
                f"Symlink creation requires Developer Mode or admin rights on Windows: {dst}\n"
                "  Enable Developer Mode: Settings → System → For Developers → Developer Mode"
            )
        else:
            warn(f"Failed to create symlink {dst} → {src}: {exc}")
        return False


def create_symlinks(name: str, skill_dir: Path) -> None:
    for link_dir in _get_llm_skill_dirs():
        _safe_symlink(skill_dir, link_dir / name)


def remove_symlinks(name: str) -> None:
    for link_dir in _get_llm_skill_dirs():
        link = link_dir / name
        if link.is_symlink():
            link.unlink()


def symlinks_exist(name: str) -> bool:
    return any((d / name).is_symlink() for d in _get_llm_skill_dirs())


def create_staging_symlinks(name: str, skill_dir: Path) -> None:
    for link_dir in _get_staging_dirs():
        link_dir.mkdir(parents=True, exist_ok=True)
        _safe_symlink(skill_dir, link_dir / name)


def remove_staging_symlinks(name: str) -> None:
    for link_dir in _get_staging_dirs():
        link = link_dir / name
        if link.is_symlink():
            link.unlink()


def staging_symlinks_exist(name: str) -> bool:
    return any((d / name).is_symlink() for d in _get_staging_dirs())


# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------

_RESERVED = {"review", "deactivated", "staging", "decommissioned", "sme", "workflow"}
_NAME_RE = re.compile(r"^[a-z][a-z0-9-]+$")


def _validate_skill_name(name: str) -> None:
    if not _NAME_RE.match(name):
        die(f"Invalid skill name '{name}'. Names must match: ^[a-z][a-z0-9-]+$")
    if name in _RESERVED:
        die(f"Invalid skill name '{name}' (reserved path)")


def _is_valid_skill_basename(name: str) -> bool:
    if name in _RESERVED or name == "README.md":
        return False
    return bool(re.match(r"^[a-z][a-z0-9-]*$", name))


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def find_skill_dir(name: str) -> Path:
    _validate_skill_name(name)
    skills_dir = _get_skills_dir()
    d = skills_dir / name
    if d.is_dir():
        return d
    die(f"Skill '{name}' not found in {skills_dir}")


def read_metadata_status(skill_md: Path) -> str:
    """Extract metadata.status from SKILL.md frontmatter."""
    if not skill_md.exists():
        return ""
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return ""

    delim_count = 0
    in_metadata = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "---":
            delim_count += 1
            if delim_count > 1:
                break
            continue
        if delim_count < 1:
            continue
        if stripped == "metadata:":
            in_metadata = True
            continue
        if in_metadata:
            m = re.match(r"^\s+status:\s*(.+)", line)
            if m:
                return m.group(1).strip().strip("\"'")
            # Exit metadata block at un-indented non-empty line
            if line and not line[0].isspace():
                in_metadata = False

    return ""


def skill_status_from_dir(d: Path) -> str:
    """Return canonical status: active|staging|review|deactivated|decommissioned|invalid."""
    raw = read_metadata_status(d / "SKILL.md").lower()
    if not raw:
        raw = "active"
    if raw in ("active", "staging", "review", "deactivated", "decommissioned"):
        return raw
    return "invalid"


def list_all_skill_dirs() -> list[Path]:
    skills_dir = _get_skills_dir()
    result = []
    if not skills_dir.is_dir():
        return result
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        if not _is_valid_skill_basename(entry.name):
            continue
        if not (entry / "SKILL.md").exists():
            continue
        result.append(entry)
    return result


# ---------------------------------------------------------------------------
# Frontmatter validation
# ---------------------------------------------------------------------------

def validate_skill_md(skill_md: Path) -> int:
    """Validate SKILL.md frontmatter. Returns number of errors found."""
    errors = 0
    dir_name = skill_md.parent.name
    expected_name = dir_name

    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        warn(f"  Cannot read {skill_md}")
        return 1

    lines = text.splitlines()

    # Extract name: from frontmatter
    fm_name = ""
    for line in lines:
        if re.match(r"^name:\s*", line):
            fm_name = re.sub(r"^name:\s*", "", line).strip().strip("\"'")
            break

    if not fm_name:
        warn(f"  MISSING FIELD: 'name' in {skill_md}")
        errors += 1
    elif fm_name != expected_name:
        warn(f"  NAME MISMATCH: frontmatter 'name: {fm_name}' vs directory '{expected_name}'")
        errors += 1

    if not any(re.match(r"^\s+version:", line) for line in lines):
        warn(f"  MISSING FIELD: 'version' in {skill_md}")
        errors += 1

    if not any(re.match(r"^metadata:", line) for line in lines):
        warn(f"  MISSING BLOCK: 'metadata:' in {skill_md}")
        errors += 1

    if not any(re.match(r"^\s+disable-model-invocation:\s*true", line) for line in lines):
        warn(f"  MISSING FLAG: 'metadata.disable-model-invocation: true' in {skill_md}")
        errors += 1

    # Optional: validate status value when set
    raw_st = read_metadata_status(skill_md).lower()
    if raw_st and raw_st not in ("active", "staging", "review", "deactivated", "decommissioned"):
        warn(f"  INVALID: metadata.status '{raw_st}' in {skill_md}")
        errors += 1

    return errors


# ---------------------------------------------------------------------------
# SHA256
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
        return h.hexdigest()
    except OSError:
        return ""


# ---------------------------------------------------------------------------
# SME context regeneration
# ---------------------------------------------------------------------------

def _regen_sme_context() -> None:
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        return
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        if not _is_valid_skill_basename(skill_dir.name):
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue
        if skill_status_from_dir(skill_dir) != "active":
            continue

        context_file = skill_dir / "context.md"
        wf_dir = skill_dir / "workflows"
        if wf_dir.is_dir():
            wf_files = sorted(wf_dir.glob("*.md"))
            lines = [
                f"# Workflows — {skill_dir.name}\n",
                "\n",
                "_Auto-generated by `skillmanager audit`._\n",
                "\n",
            ]
            for f in wf_files:
                rel = f.relative_to(skill_dir)
                lines.append(f"- `{rel}`\n")
            context_file.write_text("".join(lines), encoding="utf-8")
        else:
            context_file.write_text("<!-- No workflows/ in this skill. -->\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Command: ls
# ---------------------------------------------------------------------------

def cmd_ls(_args: list[str]) -> None:
    info("Listing all skills — metadata.status and symlink health")
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    dirs = list_all_skill_dirs()
    if not dirs:
        info(f"No skills found in {skills_dir}")
        return

    print(f"{BOLD}{'SKILL':<40} {'STATUS':<16} SYMLINKS{RESET}")
    print(f"{'─'*40} {'─'*16} {'─'*8}")

    for d in dirs:
        name = d.name
        st = skill_status_from_dir(d)
        st_show = f"{RED}invalid{RESET}" if st == "invalid" else st

        if st == "active":
            sym = f"{GREEN}ok{RESET}" if symlinks_exist(name) else f"{RED}MISSING{RESET}"
        elif st == "staging":
            if symlinks_exist(name):
                sym = f"{YELLOW}STALE-PROD{RESET}"
            elif staging_symlinks_exist(name):
                sym = f"{CYAN}ok (staging){RESET}"
            else:
                sym = f"{RED}MISSING{RESET}"
        else:
            sym = f"{YELLOW}STALE{RESET}" if symlinks_exist(name) else "-"

        print(f"{name:<40} {st_show:<16} {sym}")


# ---------------------------------------------------------------------------
# Command: status
# ---------------------------------------------------------------------------

def cmd_status(_args: list[str]) -> None:
    info("Verifying metadata.status ↔ symlink invariant for all skills")
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    violations = 0
    total = 0

    print(f"{BOLD}{'SKILL':<40} {'STATUS':<16} RESULT{RESET}")
    print(f"{'─'*40} {'─'*16} {'─'*8}")

    for d in list_all_skill_dirs():
        name = d.name
        st = skill_status_from_dir(d)
        total += 1

        prod_ok = any((ld / name).is_symlink() and (ld / name).exists() for ld in _get_llm_skill_dirs())
        staging_ok = any((sd / name).is_symlink() and (sd / name).exists() for sd in _get_staging_dirs())
        stale_prod = any((ld / name).is_symlink() for ld in _get_llm_skill_dirs())
        stale_stage = any((sd / name).is_symlink() for sd in _get_staging_dirs())

        if st == "active":
            if prod_ok:
                msg = f"{GREEN}OK — symlinks valid{RESET}"
            else:
                msg = f"{RED}VIOLATION — missing symlinks{RESET}"
                violations += 1
        elif st == "staging":
            if stale_prod:
                msg = f"{YELLOW}VIOLATION — stale production symlinks{RESET}"
                violations += 1
            elif staging_ok:
                msg = f"{GREEN}OK — staging symlinks valid{RESET}"
            else:
                msg = f"{RED}VIOLATION — missing staging symlinks{RESET}"
                violations += 1
        else:
            if st == "invalid":
                msg = f"{YELLOW}VIOLATION — invalid status + symlinks{RESET}" if (stale_prod or stale_stage) \
                    else f"{RED}VIOLATION — invalid metadata.status{RESET}"
                violations += 1
            elif stale_prod or stale_stage:
                msg = f"{YELLOW}VIOLATION — stale symlinks{RESET}"
                violations += 1
            else:
                msg = "OK — no LLM symlinks (expected)"

        print(f"{name:<40} {st:<16} {msg}")

    print()
    if violations == 0:
        ok(f"All {total} skills are consistent.")
    else:
        warn(f"{violations} violation(s) found. Run 'skillmanager audit' to fix.")


# ---------------------------------------------------------------------------
# Command: audit
# ---------------------------------------------------------------------------

def cmd_audit(_args: list[str]) -> None:
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    fixed = 0
    flagged = 0

    print(f"\n{BOLD}=== Symlink Invariant Check ==={RESET}")

    for d in list_all_skill_dirs():
        name = d.name
        st = skill_status_from_dir(d)
        prod_dirs = _get_llm_skill_dirs()
        stage_dirs = _get_staging_dirs()

        if st == "active":
            needs_fix = False
            for ld in prod_dirs:
                link = ld / name
                if not link.is_symlink():
                    needs_fix = True
                elif link.resolve() != d.resolve():
                    needs_fix = True
            if needs_fix:
                print(f"  Fixing symlinks for active skill: {name}")
                create_symlinks(name, d)
                fixed += 1
            else:
                print(f"  OK: {name}")
            remove_staging_symlinks(name)

        elif st == "staging":
            removed_prod = False
            for ld in prod_dirs:
                link = ld / name
                if link.is_symlink():
                    link.unlink()
                    removed_prod = True
            if removed_prod:
                print(f"  Removed stale production symlinks: {name}")
                fixed += 1

            staging_fix = False
            for sd in stage_dirs:
                link = sd / name
                if not link.is_symlink():
                    staging_fix = True
                elif link.resolve() != d.resolve():
                    staging_fix = True
            if staging_fix:
                print(f"  Fixing staging symlinks for: {name}")
                create_staging_symlinks(name, d)
                fixed += 1
            else:
                print(f"  OK (staged): {name}")

        else:
            removed = False
            for ld in prod_dirs + stage_dirs:
                link = ld / name
                if link.is_symlink():
                    link.unlink()
                    removed = True
            if removed:
                print(f"  Removed stale symlinks: {name} ({st})")
                fixed += 1

    print(f"\n{BOLD}=== Orphan Symlink Check ==={RESET}")
    for link_dir in _get_llm_skill_dirs() + _get_staging_dirs():
        if not link_dir.is_dir():
            continue
        for link in link_dir.iterdir():
            if not link.is_symlink():
                continue
            if not (skills_dir / link.name).is_dir():
                warn(f"  ORPHAN in {link_dir}: '{link.name}' has no matching skill directory")
                flagged += 1

    print(f"\n{BOLD}=== SKILL.md Frontmatter Check ==={RESET}")
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        if "workflows" in skill_md.parts:
            continue
        name = skill_md.parent.name
        errs = validate_skill_md(skill_md)
        if errs == 0:
            print(f"  OK: {name}")
        else:
            flagged += errs

    print(f"\n{BOLD}=== SME Context Regeneration ==={RESET}")
    _regen_sme_context()
    ok("SME context.md files updated.")

    print()
    ok(f"Audit complete. Fixed: {fixed}. Flagged for manual review: {flagged}.")


# ---------------------------------------------------------------------------
# Command: doctor
# ---------------------------------------------------------------------------

def cmd_doctor(_args: list[str]) -> None:
    print(f"\n{BOLD}=== Doctor: Environment Check ==={RESET}\n")
    issues = 0
    skillmanager_dir = _get_skillmanager_dir()
    config_file = _get_config_file()
    skills_dir = _get_skills_dir()

    def check(label: str, result: bool, ok_msg: str, fail_msg: str) -> None:
        nonlocal issues
        status = f"{GREEN}{ok_msg}{RESET}" if result else f"{YELLOW}{fail_msg}{RESET}"
        print(f"  {label:<42} {status}")
        if not result:
            issues += 1

    print(f"  SKILLMANAGER_DIR = {skillmanager_dir}\n")

    check("Config file", config_file.exists(), "found", f"MISSING — run install.py")
    check("Install directory", skillmanager_dir.is_dir(), "exists", "MISSING — run install.py")
    check("Skills directory", skills_dir.is_dir(), "exists", f"MISSING: {skills_dir}")

    for d in _get_llm_skill_dirs():
        check(f"  {d}", d.is_dir(), "exists", "MISSING")
        staging = Path(str(d).replace("skills", "skills-staging"))
        check(f"  {staging} (staging)", staging.is_dir(), "exists", "not created yet (optional)")

    if skills_dir.is_dir():
        check("Skills directory writable", os.access(skills_dir, os.W_OK), "yes", "NO — check permissions")

    # Check skillmanager in PATH
    sm_path = shutil.which("skillmanager")
    check("skillmanager in PATH", sm_path is not None, sm_path or "yes", "not found — add to PATH")

    print("\n  Tool availability:")
    for tool in ["git", "gh", "glab", "gcloud", "terraform", "markdownlint"]:
        found = shutil.which(tool)
        status = f"{GREEN}found{RESET}" if found else f"{YELLOW}not found{RESET}"
        print(f"    {tool:<14} {status}")

    print(f"\n  Python version: {platform.python_version()}")
    print(f"  Platform:       {sys.platform}\n")
    if issues == 0:
        ok("Doctor: no issues found.")
    else:
        warn(f"Doctor: {issues} issue(s) found.")


# ---------------------------------------------------------------------------
# Command: knowledge-os
# ---------------------------------------------------------------------------

def cmd_knowledge_os(_args: list[str]) -> None:
    print(f"\n{BOLD}=== Knowledge OS (meta vault) check ==={RESET}\n")
    issues = 0

    obs_root = _expand(os.environ.get("OBSIDIAN_ROOT", str(_HOME / "Obsidian")))
    obs_meta_env = os.environ.get("OBSIDIAN_META", "")
    obs_meta = _expand(obs_meta_env) if obs_meta_env else obs_root / "meta"
    choreokit_env = os.environ.get("CHOREOKIT_DIR", "")

    def ko_check(label: str, result: bool, ok_msg: str, fail_msg: str) -> None:
        nonlocal issues
        status = f"{GREEN}{ok_msg}{RESET}" if result else f"{YELLOW}{fail_msg}{RESET}"
        print(f"  {label:<46} {status}")
        if not result:
            issues += 1

    print(f"  OBSIDIAN_ROOT = {obs_root}")
    print(f"  OBSIDIAN_META = {obs_meta}")
    if choreokit_env:
        print(f"  CHOREOKIT_DIR = {_expand(choreokit_env)} (optional op-skills tree)")
    print()

    ko_check("Obsidian root exists", obs_root.is_dir(), "yes", "MISSING — set OBSIDIAN_ROOT")
    ko_check("Meta vault directory", obs_meta.is_dir(), "yes", "MISSING — create or set OBSIDIAN_META")
    ko_check("meta/CLAUDE.md", (obs_meta / "CLAUDE.md").exists(), "found", "MISSING")
    ko_check("meta/_os/index.md", (obs_meta / "_os" / "index.md").exists(), "found",
             "MISSING (expected for super-wiki registry)")
    ko_check("meta/wiki/", (obs_meta / "wiki").is_dir(), "exists", "MISSING")
    ko_check("meta/inbox/", (obs_meta / "inbox").is_dir(), "exists", "optional")

    vault_count = 0
    if obs_root.is_dir():
        for item in obs_root.iterdir():
            if item.is_dir() and (item / "CLAUDE.md").exists() and (item / "_os" / "index.md").exists():
                vault_count += 1
    print(f"\n  Vaults under OBSIDIAN_ROOT with CLAUDE.md + _os/index.md: {vault_count}")

    print("\n  Skillforge symlinks (wiki + vault path skills):")
    for skill_name in ["wiki-harvest", "vault-paths"]:
        found = False
        target = ""
        for ld in _get_llm_skill_dirs():
            link = ld / skill_name
            if link.is_symlink() and link.exists():
                found = True
                try:
                    target = os.readlink(link)
                except OSError:
                    target = "?"
                break
        if found:
            print(f"    {skill_name:<22} {GREEN}ok{RESET} → {target}")
        else:
            print(f"    {skill_name:<22} {YELLOW}missing — skill inactive or not audited{RESET}")
            issues += 1

    if choreokit_env:
        ck = _expand(choreokit_env)
        ko_check("CHOREOKIT_DIR", ck.is_dir(), "exists", "MISSING")
    else:
        print("\n  CHOREOKIT_DIR unset (OK if all op-skills are under ~/.claude/skills only).")

    print()
    if issues == 0:
        ok("knowledge-os: no symlink/layout issues.")
    else:
        warn(f"knowledge-os: {issues} note(s) — run 'skillmanager audit' or adjust env vars.")


# ---------------------------------------------------------------------------
# Command: git helpers
# ---------------------------------------------------------------------------

def _require_git() -> None:
    if not shutil.which("git"):
        die("'git' not found. Install Git to use this command.")
    result = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True)
    if result.returncode != 0:
        die("Not inside a git repository.")


def _git_check_staged_skill_names() -> int:
    result = subprocess.run(["git", "diff", "--cached", "--name-only"],
                            capture_output=True, text=True)
    paths = result.stdout.strip().splitlines()
    errors = 0
    for path in paths:
        m = re.match(r"^skills/([a-z][a-z0-9-]+(?:-sys)?)/", path)
        if not m:
            continue
        dir_name = m.group(1)
        if dir_name in _RESERVED:
            continue
        if not _NAME_RE.match(dir_name) or dir_name in _RESERVED:
            warn(f"Naming violation: '{dir_name}' — invalid skill directory name")
            errors += 1
    return errors


_CONV_COMMIT_RE = re.compile(
    r"^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)"
    r"(\([a-z0-9_/.-]+\))?!?: .+"
)


def _validate_commit_msg(msg: str) -> bool:
    if _CONV_COMMIT_RE.match(msg):
        return True
    warn("Commit message does not follow conventional commits format.")
    print("  Expected: type(scope): description")
    print("  Examples: feat: add git skill  |  fix(cli): handle empty input")
    print("  Types:    feat fix chore docs style refactor perf test build ci revert\n")
    answer = input("Proceed with this message anyway? [y/N]: ").strip().lower()
    return answer == "y"


def _cmd_git_commit() -> bool:
    staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                            capture_output=True, text=True).stdout.strip()
    if not staged:
        subprocess.run(["git", "status"])
        print()
        die("Nothing staged. Stage files first: skillmanager git add <files>")

    skill_files = [f for f in staged.splitlines() if f.startswith("skills/")]
    if skill_files:
        info("Staged changes include skill files — running naming check...")
        if _git_check_staged_skill_names() > 0:
            die("Skill naming check failed. Rename the violating skill directories before committing.")
        ok("Skill naming check passed.")

    print(f"\n{BOLD}=== Staged changes ==={RESET}")
    subprocess.run(["git", "diff", "--cached", "--stat"])
    print()
    subprocess.run(["git", "diff", "--cached"])

    print(f"\n{BOLD}=== Recent commits ==={RESET}")
    subprocess.run(["git", "log", "--oneline", "-5"])
    print()

    print(f"{CYAN}Enter commit message (review the diff above — or 'cancel'):{RESET}")
    msg = input("> ").strip()
    if not msg or msg == "cancel":
        info("Aborted.")
        return False

    if not _validate_commit_msg(msg):
        info("Aborted.")
        return False

    print(f"\n{BOLD}Message:{RESET} {msg}")
    answer = input("Commit? (yes / no): ").strip()
    if answer != "yes":
        info("Aborted.")
        return False

    subprocess.run(["git", "commit", "-m", msg])
    return True


def _cmd_git_push(args: list[str]) -> None:
    force = any(a in ("--force", "-f", "--force-with-lease") for a in args)
    target_branch = next((a for a in args if a in ("main", "master")), None)

    if target_branch is None:
        result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"],
                                capture_output=True, text=True)
        branch = result.stdout.strip()
        if branch in ("main", "master"):
            target_branch = branch

    if force and target_branch:
        print(f"{RED}[CONFIRM]{RESET} Force-push to '{target_branch}' may overwrite others' work.")
        answer = input("           Type 'yes' to proceed, anything else to cancel: ").strip()
        if answer != "yes":
            info("Aborted.")
            return

    subprocess.run(["git", "push"] + args)


def _cmd_git_all() -> None:
    print(f"{BOLD}=== Working tree status ==={RESET}")
    subprocess.run(["git", "status"])
    print()

    staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                            capture_output=True, text=True).stdout.strip()
    if not staged:
        modified = subprocess.run(["git", "diff", "--name-only"],
                                  capture_output=True, text=True).stdout.strip()
        if not modified:
            info("Nothing to commit — working tree clean.")
            return

        print(f"{BOLD}=== Modified files to stage ==={RESET}")
        print(modified)
        answer = input("\nStage all modified tracked files? (yes / no): ").strip()
        if answer != "yes":
            info("Aborted. Stage files manually with: skillmanager git add <files>")
            return
        for f in modified.splitlines():
            subprocess.run(["git", "add", "--", f])
        ok("Files staged.")
        print()

    if not _cmd_git_commit():
        return

    result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"],
                            capture_output=True, text=True)
    branch = result.stdout.strip()
    answer = input(f"\n{CYAN}Push '{branch}' to origin?{RESET} (yes / no): ").strip()
    if answer != "yes":
        info("Commit saved locally. Push later with: skillmanager git push")
        return

    subprocess.run(["git", "push", "origin", branch])
    ok(f"Pushed: {branch} → origin")


def _cmd_git_pr(args: list[str]) -> None:
    if not shutil.which("gh"):
        die("'gh' not found. Install the GitHub CLI: brew install gh")
    subprocess.run(["gh", "pr", "create"] + args)


def _cmd_git_mr(args: list[str]) -> None:
    if not shutil.which("glab"):
        die("'glab' not found. Install the GitLab CLI: brew install glab")
    subprocess.run(["glab", "mr", "create"] + args)


def _cmd_git_repo_create() -> None:
    provider = ""
    result = subprocess.run(["git", "remote", "get-url", "origin"],
                            capture_output=True, text=True)
    if result.returncode == 0:
        url = result.stdout.strip()
        if "github.com" in url:
            provider = "github"
        elif "gitlab.com" in url:
            provider = "gitlab"

    if not provider:
        choice = input("Provider? (1) GitHub  (2) GitLab: ").strip()
        if choice == "1":
            provider = "github"
        elif choice == "2":
            provider = "gitlab"
        else:
            die("Invalid choice.")

    repo_name = input("Repository name: ").strip()
    if not repo_name:
        die("Repository name is required.")

    vis_choice = input("Visibility — (1) Private [default]  (2) Public: ").strip()
    visibility = "public" if vis_choice == "2" else "private"
    description = input("Description (optional): ").strip()

    print(f"\n{BOLD}Create repository:{RESET}")
    print(f"  Provider:    {provider}")
    print(f"  Name:        {repo_name}")
    print(f"  Visibility:  {visibility}")
    if description:
        print(f"  Description: {description}")

    if input("\nProceed? (yes / no): ").strip() != "yes":
        info("Aborted.")
        return

    if provider == "github":
        if not shutil.which("gh"):
            die("'gh' not found. Install: brew install gh")
        gh_args = ["repo", "create", repo_name, f"--{visibility}", "--source=.", "--remote=origin"]
        if description:
            gh_args += ["--description", description]
        subprocess.run(["gh"] + gh_args)
        ok(f"GitHub repository '{repo_name}' created.")
    else:
        if not shutil.which("glab"):
            die("'glab' not found. Install: brew install glab")
        glab_args = ["repo", "create", repo_name]
        glab_args.append("--private" if visibility == "private" else "--public")
        if description:
            glab_args += ["--description", description]
        subprocess.run(["glab"] + glab_args)

        user_result = subprocess.run(["glab", "api", "user", "--jq", ".username"],
                                     capture_output=True, text=True)
        glab_user = user_result.stdout.strip()
        if glab_user:
            new_url = f"git@gitlab.com:{glab_user}/{repo_name}.git"
            remote_result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True)
            if remote_result.returncode == 0:
                subprocess.run(["git", "remote", "set-url", "origin", new_url])
            else:
                subprocess.run(["git", "remote", "add", "origin", new_url])
            ok(f"Remote 'origin' set to: {new_url}")
        ok(f"GitLab repository '{repo_name}' created.")


def _cmd_git_repo_rename() -> None:
    result = subprocess.run(["git", "remote", "get-url", "origin"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        die("No 'origin' remote found.")
    remote_url = result.stdout.strip()

    if "github.com" in remote_url:
        provider = "github"
    elif "gitlab.com" in remote_url:
        provider = "gitlab"
    else:
        die(f"Remote 'origin' does not appear to be GitHub or GitLab: {remote_url}")

    # Parse owner and repo from URL
    if remote_url.startswith("git@"):
        proto = "ssh"
        m = re.search(r"[:/]([^/]+)/([^/]+?)(?:\.git)?$", remote_url)
    else:
        proto = "https"
        m = re.search(r"/([^/]+)/([^/]+?)(?:\.git)?$", remote_url)

    if not m:
        die(f"Could not parse repository name from remote URL: {remote_url}")
    owner, old_name = m.group(1), m.group(2)

    print(f"Current repository: {owner}/{old_name} ({provider})")
    new_name = input("New name: ").strip()
    if not new_name:
        die("New name is required.")
    if new_name == old_name:
        info("Name is unchanged.")
        return

    if proto == "ssh":
        new_remote_url = f"git@{provider}.com:{owner}/{new_name}.git"
    else:
        new_remote_url = f"https://{provider}.com/{owner}/{new_name}.git"

    print(f"\n{BOLD}Rename repository:{RESET}")
    print(f"  Provider:       {provider}")
    print(f"  Old name:       {old_name}")
    print(f"  New name:       {new_name}")
    print(f"  New remote URL: {new_remote_url}")

    if input("\nProceed? (yes / no): ").strip() != "yes":
        info("Aborted.")
        return

    if provider == "github":
        if not shutil.which("gh"):
            die("'gh' not found. Install: brew install gh")
        subprocess.run(["gh", "repo", "rename", new_name])
    else:
        if not shutil.which("glab"):
            die("'glab' not found. Install: brew install glab")
        subprocess.run(["glab", "api", f"projects/{owner}%2F{old_name}",
                        "-X", "PUT", f"-f=name={new_name}", f"-f=path={new_name}"])

    subprocess.run(["git", "remote", "set-url", "origin", new_remote_url])
    ok(f"Repository renamed to '{new_name}'.")
    ok(f"Remote 'origin' updated to: {new_remote_url}")
    subprocess.run(["git", "remote", "-v"])


def cmd_git(args: list[str]) -> None:
    if not shutil.which("git"):
        die("'git' not found. Install Git to use this command.")
    if not args:
        print("Usage: skillmanager git <command> [args...]\nRun 'skillmanager help git' for available commands.")
        sys.exit(1)

    subcmd = args[0]
    rest = args[1:]

    if subcmd == "commit":
        _require_git(); _cmd_git_commit()
    elif subcmd == "push":
        _require_git(); _cmd_git_push(rest)
    elif subcmd == "all":
        _require_git(); _cmd_git_all()
    elif subcmd == "pr":
        _require_git(); _cmd_git_pr(rest)
    elif subcmd == "mr":
        _require_git(); _cmd_git_mr(rest)
    elif subcmd == "repo-create":
        _cmd_git_repo_create()
    elif subcmd == "repo-rename":
        _require_git(); _cmd_git_repo_rename()
    else:
        _require_git()
        subprocess.run(["git", subcmd] + rest)


# ---------------------------------------------------------------------------
# Command: update
# ---------------------------------------------------------------------------

def cmd_update(args: list[str]) -> None:
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    skillmanager_dir = _get_skillmanager_dir()
    checksums_file = skillmanager_dir / ".checksums"
    version_file = skillmanager_dir / ".install-version"
    staging_dir = skillmanager_dir / "staging"
    staging_manifest = skillmanager_dir / ".staging-manifest"

    source_path: Path | None = None
    i = 0
    while i < len(args):
        if args[i] == "--source" and i + 1 < len(args):
            source_path = _expand(args[i + 1])
            i += 2
        else:
            die(f"Unknown argument: {args[i]}. Usage: skillmanager update --source <path>")

    if source_path is None:
        die("Usage: skillmanager update --source <path>\n"
            "  <path>  Directory containing a skills/ subdirectory to apply updates from.")

    if not source_path.is_dir():
        die(f"Source path not found: {source_path}")
    if not (source_path / "skills").is_dir():
        die(f"No skills/ subdirectory found in: {source_path}")

    print(f"\n{BOLD}=== Skill Forge Update ==={RESET}\n")
    print(f"  Source:      {source_path}")
    print(f"  Install dir: {skillmanager_dir}\n")

    updated = 0
    staged = 0

    for src_file in sorted((source_path / "skills").rglob("*")):
        if not src_file.is_file():
            continue
        rel = src_file.relative_to(source_path / "skills")
        installed_file = skills_dir / rel

        if not installed_file.exists():
            installed_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, installed_file)
            ok(f"New: {rel}")
            updated += 1
            continue

        new_hash = sha256_file(src_file)
        current_hash = sha256_file(installed_file)

        if new_hash == current_hash:
            continue

        install_hash = ""
        if checksums_file.exists():
            for line in checksums_file.read_text(encoding="utf-8").splitlines():
                if line.endswith(f"  skills/{rel}"):
                    install_hash = line.split()[0]
                    break

        if not install_hash or current_hash == install_hash:
            shutil.copy2(src_file, installed_file)
            # Update checksum entry
            lines = []
            if checksums_file.exists():
                lines = [l for l in checksums_file.read_text(encoding="utf-8").splitlines()
                         if not l.endswith(f"  skills/{rel}")]
            lines.append(f"{new_hash}  skills/{rel}")
            checksums_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            ok(f"Updated: {rel}")
            updated += 1
        else:
            stage_path = staging_dir / "skills" / rel
            stage_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, stage_path)
            with staging_manifest.open("a", encoding="utf-8") as f:
                f.write(f"{rel}\n")
            warn(f"Staged (customised): {rel}")
            staged += 1

    _regen_sme_context()
    version_file.write_text(
        datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") + "\n", encoding="utf-8"
    )

    print()
    ok(f"Update complete. Updated in place: {updated}. Staged for review: {staged}.")
    if staged > 0:
        info("Run 'skillmanager staging ls' to review staged updates.")


# ---------------------------------------------------------------------------
# Command: staging
# ---------------------------------------------------------------------------

def cmd_staging(args: list[str]) -> None:
    subcommand = args[0] if args else "ls"
    rest = args[1:] if len(args) > 1 else []
    skillmanager_dir = _get_skillmanager_dir()
    staging_dir = skillmanager_dir / "staging"
    staging_manifest = skillmanager_dir / ".staging-manifest"
    skills_dir = _get_skills_dir()

    if subcommand == "ls":
        print(f"\n{BOLD}=== Staged Updates ==={RESET}\n")
        if not staging_manifest.exists() or not staging_manifest.stat().st_size:
            info("No staged updates. Run 'skillmanager update' to check for new versions.")
            return
        for rel in staging_manifest.read_text(encoding="utf-8").splitlines():
            if not rel:
                continue
            staged = staging_dir / "skills" / rel
            suffix = "[staged]" if staged.exists() else "[staged — file missing, run dismiss]"
            print(f"  {rel:<50}  {suffix}")

    elif subcommand == "diff":
        if not rest:
            die("Usage: skillmanager staging diff <skill-name>")
        name = rest[0]
        _validate_skill_name(name)
        rel = next((l for l in (staging_manifest.read_text(encoding="utf-8").splitlines()
                                if staging_manifest.exists() else [])
                    if f"/{name}/" in l), None)
        if not rel:
            die(f"No staged update found for '{name}'.")
        staged = staging_dir / "skills" / rel
        if not staged.exists():
            die(f"Staged file not found: {staged}")
        installed = skills_dir / rel
        print(f"{BOLD}Diff: {rel}{RESET}")
        subprocess.run(["diff", "--color=auto", str(installed), str(staged)])

    elif subcommand in ("accept", "dismiss"):
        if not rest:
            die(f"Usage: skillmanager staging {subcommand} <skill-name>")
        name = rest[0]
        _validate_skill_name(name)
        lines = staging_manifest.read_text(encoding="utf-8").splitlines() if staging_manifest.exists() else []
        rel = next((l for l in lines if f"/{name}/" in l), None)
        if not rel:
            die(f"No staged update found for '{name}'.")
        staged = staging_dir / "skills" / rel
        if subcommand == "accept":
            if not staged.exists():
                die(f"Staged file not found: {staged}")
            shutil.copy2(staged, skills_dir / rel)
            staged.unlink()
            ok(f"Accepted: {rel} — installed file updated.")
        else:
            if staged.exists():
                staged.unlink()
            ok(f"Dismissed: {rel} — staged version discarded, current file kept.")
        remaining = [l for l in lines if l != rel]
        staging_manifest.write_text("\n".join(remaining) + ("\n" if remaining else ""), encoding="utf-8")

    else:
        die(f"Unknown staging subcommand: '{subcommand}'. Use: ls, diff <name>, accept <name>, dismiss <name>")


# ---------------------------------------------------------------------------
# Command: customize
# ---------------------------------------------------------------------------

def cmd_customize(_args: list[str]) -> None:
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    print(f"\n{BOLD}=== Skill Forge Customize ==={RESET}\n")
    print("This wizard helps you create environment-specific context and workflow")
    print("skills for your installed SMEs.\n")
    print("For each skill you will be asked:")
    print("  1. Whether to add an environment-specific reference file.")
    print("  2. Whether to scaffold a companion skill.\n")

    created_refs = 0
    created_wfs = 0

    for sme_dir in sorted(skills_dir.iterdir()):
        if not sme_dir.is_dir():
            continue
        sme_name = sme_dir.name
        if not _is_valid_skill_basename(sme_name):
            continue
        if not (sme_dir / "SKILL.md").exists():
            continue

        print(f"{BOLD}--- {sme_name} ---{RESET}")

        refs_dir = sme_dir / "references"
        env_ref = refs_dir / f"{sme_name}-env.md"

        if env_ref.exists():
            info(f"Reference already exists: {env_ref} — skipping.")
        else:
            ans_ref = input(f"Create environment-specific reference for {sme_name}? [y/N]: ").strip().lower()
            if ans_ref == "y":
                env_context = input("Describe the environment context:\n> ").strip()
                refs_dir.mkdir(parents=True, exist_ok=True)
                content = (
                    f"# {sme_name} — Environment Context\n\n"
                    "_Created by `skillmanager customize`. Edit this file with your specific environment details._\n\n"
                    f"## Context\n\n{env_context or '<add your environment context here>'}\n\n"
                    "## Notes\n\n- Add platform-specific details, account IDs, resource naming conventions, etc.\n"
                )
                env_ref.write_text(content, encoding="utf-8")
                ok(f"Created: {env_ref}")
                created_refs += 1

        ans_wf = input(f"Create a custom workflow skill for {sme_name}? [y/N]: ").strip().lower()
        if ans_wf == "y":
            env_name = input("Environment name for workflow (e.g. 'gcp', 'aws', 'azure'): ").strip()
            env_name = env_name.lower().replace(" ", "-")
            if not env_name:
                warn("No environment name provided — skipping workflow creation.")
            else:
                wf_name = f"{sme_name}-{env_name}"
                wf_dir = skills_dir / wf_name
                if wf_dir.is_dir():
                    info(f"Workflow already exists: {wf_name} — skipping.")
                else:
                    wf_dir.mkdir(parents=True, exist_ok=True)
                    skill_content = (
                        "---\n"
                        f"name: {wf_name}\n"
                        f"description: {env_name} environment-specific workflow for {sme_name} operations.\n"
                        "metadata:\n"
                        '  version: "1.0"\n'
                        "  status: active\n"
                        "  disable-model-invocation: true\n"
                        "---\n\n"
                        f"# {env_name} {sme_name} Workflow\n\nEdit this file to define the workflow steps.\n"
                    )
                    (wf_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
                    create_symlinks(wf_name, wf_dir)
                    remove_staging_symlinks(wf_name)
                    ok(f"Created and linked: {wf_name} (metadata.status: active)")
                    created_wfs += 1

        print()

    _regen_sme_context()

    print(f"\n{BOLD}=== Customize Complete ==={RESET}\n")
    print(f"  Reference files created:  {created_refs}")
    print(f"  Workflow skills created:  {created_wfs}\n")
    if created_wfs > 0:
        info("New workflow skills are active. SME context.md files have been updated.")
        info("Run 'skillmanager ls' to confirm, or 'skillmanager audit' to verify invariants.")
    if created_refs > 0:
        info("Edit the reference files to add your specific environment details.")
        for f in sorted(skills_dir.rglob("*-env.md")):
            print(f"  {f}")


# ---------------------------------------------------------------------------
# Command: lint
# ---------------------------------------------------------------------------

def cmd_lint(args: list[str]) -> None:
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    target = Path(args[0]) if args else None
    errors = 0

    print(f"\n{BOLD}=== Lint: Markdown Quality Check ==={RESET}\n")

    if shutil.which("markdownlint"):
        info("Using markdownlint")
        if target:
            result = subprocess.run(["markdownlint", str(target)])
            errors = result.returncode
        else:
            for f in sorted(skills_dir.rglob("*.md")):
                result = subprocess.run(["markdownlint", str(f)])
                if result.returncode != 0:
                    errors += 1
    else:
        warn("markdownlint not found — running basic checks only.")

        def lint_file(path: Path) -> int:
            file_errors = 0
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                return 0
            lines = text.splitlines()
            if path.name == "SKILL.md":
                if not (lines and lines[0].strip() == "---"):
                    warn(f"  [LINT] Missing frontmatter: {path}")
                    file_errors += 1
            if any(l.rstrip() != l and l.endswith(" ") for l in lines):
                warn(f"  [LINT] Trailing whitespace: {path}")
                file_errors += 1
            if path.name == "SKILL.md":
                h1 = sum(1 for l in lines if re.match(r"^# ", l))
                if h1 == 0:
                    warn(f"  [LINT] No H1 heading: {path}")
                    file_errors += 1
            if file_errors == 0:
                print(f"  OK: {path.parent.name}/{path.name}")
            return file_errors

        if target:
            errors = lint_file(target)
        else:
            for f in sorted(skills_dir.rglob("*.md")):
                errors += lint_file(f)

    print()
    if errors == 0:
        ok("Lint: no issues found.")
    else:
        warn(f"Lint: {errors} file(s) with issues.")
    sys.exit(errors)


# ---------------------------------------------------------------------------
# Command: show
# ---------------------------------------------------------------------------

def cmd_show(args: list[str]) -> None:
    if not args:
        die("Usage: skillmanager show <name>")
    skills_dir = _get_skills_dir()
    if not skills_dir.is_dir():
        die(f"Skills directory not found: {skills_dir} — run 'install.py' first.")

    name = args[0]
    _validate_skill_name(name)
    skill_dir = find_skill_dir(name)
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        die(f"SKILL.md not found in: {skill_dir}")

    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()

    fm_name = fm_desc = fm_version = ""
    for line in lines:
        if re.match(r"^name:\s*", line):
            fm_name = re.sub(r"^name:\s*", "", line).strip().strip("\"'")
        if re.match(r"^description:\s*", line):
            fm_desc = re.sub(r"^description:\s*", "", line).strip()
        if re.match(r"^\s+version:\s*", line):
            fm_version = re.sub(r"^\s+version:\s*", "", line).strip().strip("\"'")

    print(f"{BOLD}── {fm_name or name}{RESET}")
    if fm_version:
        print(f"   version:  {fm_version}")
    if fm_desc:
        print(f"   {fm_desc}")
    print()

    # Print body (after closing ---)
    delim = 0
    for line in lines:
        if line.strip() == "---":
            delim += 1
            continue
        if delim >= 2:
            print(line)


# ---------------------------------------------------------------------------
# Command: version / config
# ---------------------------------------------------------------------------

def cmd_version(_args: list[str]) -> None:
    # VERSION SYNC: keep aligned with docs/index.md "Version X.Y.Z" line
    print("skillmanager 2.0.0")


def cmd_config(args: list[str]) -> None:
    config_file = _get_config_file()
    if args and args[0] == "set":
        if len(args) < 3:
            die("Usage: skillmanager config set <key> <value>")
        key, value = args[1], args[2]
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", key):
            die(f"Invalid config key: '{key}'")
        if not config_file.exists():
            die(f"Config not found: {config_file} — run install.py first.")
        lines = config_file.read_text(encoding="utf-8").splitlines()
        updated = False
        new_lines = []
        for line in lines:
            if re.match(rf"^{re.escape(key)}:", line):
                new_lines.append(f"{key}: {value}")
                updated = True
            else:
                new_lines.append(line)
        if not updated:
            new_lines.append(f"{key}: {value}")
        config_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        ok(f"{'Updated' if updated else 'Added'}: {key} = {value}")
    else:
        if config_file.exists():
            print(config_file.read_text(encoding="utf-8"))
        else:
            warn(f"Config not found: {config_file}")
            info("Run 'python3 scripts/install.py' to create it.")


# ---------------------------------------------------------------------------
# Command: memory-help
# ---------------------------------------------------------------------------

def cmd_memory_help(_args: list[str]) -> None:
    print(f"""{BOLD}Skill Forge — Memory Guide{RESET}

{BOLD}What memory does{RESET}
  Memory files let your AI assistant remember things about you across sessions.
  Memory is loaded when the linked skill is invoked and cleared by /clear.
  You control what is saved — nothing is automatic.

{BOLD}When it loads{RESET}
  If a skill sets optional `metadata.memory-file`, that file loads with the skill.
  Most skills use `SKILL.md` as the only required brain; `persona/` and project
  CLAUDE.md hold extra context. Clear on /clear.

{BOLD}System skills{RESET}
  If you chose always-on mode at install, system capabilities (skill detection,
  memory management) are embedded in model.md and survive /clear.
  If you chose manual mode, invoke /skill-manager or /memory when needed.
  To switch modes: invoke /memory → "toggle system skills"

{BOLD}Cost implications{RESET}
  Every word loaded into a session costs tokens. Keep memory files focused.
  After /clear, only model.md remains — skill memory must be re-invoked.

{BOLD}Typical context locations{RESET}
  {_get_skillmanager_dir()}/skills/<name>/SKILL.md
  required; optional {_get_skillmanager_dir()}/skills/<name>/persona/<topic>.md""")


# ---------------------------------------------------------------------------
# Command: uninstall
# ---------------------------------------------------------------------------

def cmd_uninstall(_args: list[str]) -> None:
    skillmanager_dir = _get_skillmanager_dir()
    print(f"\n{BOLD}=== Skill Forge Uninstall ==={RESET}\n")
    print("This will remove:")
    print("  1. All skill symlinks from LLM skill directories")
    print("  2. The skillmanager binary from the install bin directory")
    print(f"  3. (Optional) Skill data directory: {skillmanager_dir}")
    print("  4. (Optional) PATH entries added to shell rc files\n")

    answer = input(f"{RED}[CONFIRM]{RESET} Type 'uninstall' to proceed, or anything else to cancel: ").strip()
    if answer != "uninstall":
        info("Aborted.")
        return

    # Step 1: Remove all symlinks
    print(f"\n{BOLD}Step 1: Removing skill symlinks...{RESET}")
    removed = 0
    for link_dir in _get_llm_skill_dirs() + _get_staging_dirs():
        if not link_dir.is_dir():
            continue
        for link in link_dir.iterdir():
            if link.is_symlink():
                link.unlink()
                ok(f"Removed: {link}")
                removed += 1
    info(f"Removed {removed} symlink(s).")

    # Step 2: Remove CLI binary
    print(f"\n{BOLD}Step 2: Removing CLI binary...{RESET}")
    if IS_WINDOWS:
        install_bin = Path(os.environ.get("LOCALAPPDATA", str(_HOME / "AppData" / "Local"))) / "Programs" / "skillmanager"
    else:
        install_bin = _HOME / ".local" / "bin" / "skillmanager"

    if install_bin.exists():
        install_bin.unlink()
        ok(f"Removed: {install_bin}")
    else:
        info(f"Binary not found at {install_bin} — skipping.")

    # Step 3: Check for customised files
    print(f"\n{BOLD}Step 3: Checking for customised files...{RESET}")
    checksums_file = skillmanager_dir / ".checksums"
    skills_dir = _get_skills_dir()
    customised = []
    if checksums_file.exists() and skills_dir.is_dir():
        checksum_map = {}
        for line in checksums_file.read_text(encoding="utf-8").splitlines():
            parts = line.split("  ", 1)
            if len(parts) == 2:
                checksum_map[parts[1]] = parts[0]
        for f in sorted(skills_dir.rglob("*")):
            if not f.is_file():
                continue
            rel = str(f.relative_to(skillmanager_dir))
            install_hash = checksum_map.get(rel, "")
            if install_hash and sha256_file(f) != install_hash:
                customised.append(rel)

    if customised:
        print(f"\n{YELLOW}Customised files detected ({len(customised)}):{RESET}")
        for c in customised:
            print(f"  - {c}")
        backup_answer = input("\nBack up customised files before uninstall? [Y/n]: ").strip() or "Y"
        if backup_answer.upper() == "Y":
            today = datetime.datetime.now().strftime("%Y%m%d")
            backup_dir = _HOME / f".skillmanager-backup-{today}"
            for rel in customised:
                src = skillmanager_dir / rel
                dst = backup_dir / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
            ok(f"Customised files backed up to: {backup_dir}")
    else:
        info("No customised files detected.")

    # Step 4: Optionally remove skill data
    print(f"\n{BOLD}Step 4: Skill data{RESET} — {skillmanager_dir}")
    if input("Remove skill data? Deletes all skills, memory, and config. (yes / no): ").strip() == "yes":
        shutil.rmtree(skillmanager_dir, ignore_errors=True)
        ok(f"Removed: {skillmanager_dir}")
    else:
        info(f"Kept: {skillmanager_dir}")

    # Step 5: Remove PATH entries from shell rc files (Unix only)
    if not IS_WINDOWS:
        print(f"\n{BOLD}Step 5: Shell PATH entries{RESET}")
        if input("Remove Skill Forge PATH entries from ~/.bashrc and ~/.zshrc? (yes / no): ").strip() == "yes":
            path_line = 'export PATH="$HOME/.local/bin:$PATH"'
            path_comment = "# Added by Skill Forge install"
            for rc_name in (".bashrc", ".zshrc"):
                rc_file = _HOME / rc_name
                if not rc_file.exists():
                    continue
                lines = [l for l in rc_file.read_text(encoding="utf-8").splitlines()
                         if path_comment not in l and path_line not in l]
                rc_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
                ok(f"Cleaned: {rc_file}")
        else:
            info("Kept PATH entries in shell config files.")

    print()
    ok("Skill Forge uninstalled. Reload your shell if needed.")


# ---------------------------------------------------------------------------
# Usage / help
# ---------------------------------------------------------------------------

def _usage() -> str:
    return f"""{BOLD}skillmanager{RESET} — LLM skill symlink manager

{BOLD}USAGE{RESET}
  skillmanager <command> [args]

{BOLD}SKILL MANAGEMENT{RESET}
  ls                     List skills: metadata.status vs symlink health
  status                 Verify status ↔ symlinks (metadata in SKILL.md)
  audit, sync            Repair symlinks to match each skill's metadata.status
  show <name>            Display SKILL.md for a skill
  lint [file]            Check markdown quality
  doctor                 Self-check paths, tools, permissions, and PATH
  knowledge-os           Check Obsidian meta layout + wiki/vault skills symlinks
  config                 Show current configuration
  config set <k> <v>     Update a configuration value
  memory-help            Guide to memory files and token costs
  version                Print version

  Edit {BOLD}metadata.status{RESET} in skills/<name>/SKILL.md, then run {BOLD}skillmanager audit{RESET}.
  Status values: active (default) | staging | review | deactivated | decommissioned

{BOLD}GIT{RESET}
  git status             Show working tree status
  git log [args]         Show commit history
  git diff [args]        Show unstaged or staged changes
  git add <files>        Stage files for commit
  git commit             Diff-driven commit: show diff → prompt message → confirm → commit
  git push [args]        Push; blocks unconfirmed force-push to main/master
  git all                Stage modified files → commit (diff-driven) → push
  git pull [args]        Pull from remote
  git branch [args]      List or manage branches
  git checkout <branch>  Switch to a branch
  git clone <url>        Clone a repository
  git tag [args]         List or manage tags
  git pr [args]          Create a GitHub pull request (requires gh)
  git mr [args]          Create a GitLab merge request (requires glab)
  git repo-create        Create a new GitHub or GitLab repository
  git repo-rename        Rename a repository and update the local remote URL
  git <other> [args]     Any other git command passed through directly

  update --source <path> Apply skill updates from a directory; stages customised files
  uninstall              Remove symlinks, binary, and optionally all skill data

{BOLD}SKILL LOCATIONS{RESET}
  Every skill:   skills/<name>/

{BOLD}ENVIRONMENT{RESET}
  SKILLMANAGER_DIR   Override install directory (default: read from config.yaml)
  OBSIDIAN_ROOT      Base path for Obsidian vaults (default: ~/Obsidian)
  OBSIDIAN_META      Master meta vault (default: OBSIDIAN_ROOT/meta)
  CHOREOKIT_DIR      Optional separate tree for Knowledge OS op-skills

{BOLD}PLATFORM NOTES{RESET}
  Symlinks on Windows require Developer Mode or administrator rights.
  PATH is configured via ~/.bashrc / ~/.zshrc on Unix/macOS.
  On Windows, add the install directory to PATH via System Properties.

{BOLD}EXAMPLES{RESET}
  skillmanager ls
  skillmanager audit
  skillmanager doctor"""


def cmd_help(args: list[str]) -> None:
    subcmd = args[0] if args else ""
    if subcmd == "git":
        print(f"""{BOLD}skillmanager git <command> [args]{RESET}
Run git commands with skill-manager safety gates:

  commit      — diff → message prompt → conventional-commit check → confirm → commit
  all         — stage modified files → commit (diff-driven) → push
  push        — blocks unconfirmed force-push to main/master
  pr          — create a GitHub PR via gh (requires: gh auth login)
  mr          — create a GitLab MR via glab (requires: glab auth login)
  repo-create — create a new GitHub or GitLab repository
  repo-rename — rename repo on platform and update local remote URL
  <other>     — passed directly to git

Examples:
  skillmanager git all
  skillmanager git commit
  skillmanager git push origin feat/my-branch
  skillmanager git pr --title "feat: add new skill"
  skillmanager git repo-create
  skillmanager git repo-rename""")
    elif subcmd == "uninstall":
        print(f"""{BOLD}skillmanager uninstall{RESET}
Interactively removes Skill Forge from the system:
  1. Removes all skill symlinks from LLM target directories
  2. Removes the skillmanager binary from the install bin directory
  3. (Optional) Removes skill data directory ({_get_skillmanager_dir()})
  4. (Optional) Removes PATH entries from shell rc files (Unix/macOS)

Requires typing 'uninstall' to confirm. Skill data is never deleted without
a second explicit confirmation.""")
    elif subcmd in ("audit", "sync"):
        print(f"""{BOLD}skillmanager audit{RESET} (alias: {BOLD}skillmanager sync{RESET})
Recreate symlinks from metadata.status in each skills/<name>/SKILL.md.
  - active (default) — production LLM dirs; strip staging links
  - staging — skills-staging dirs only
  - review / deactivated / decommissioned — no LLM symlinks
Also: orphan symlink warnings, frontmatter check, regen context.md for active skills.""")
    elif subcmd == "knowledge-os":
        print(f"""{BOLD}skillmanager knowledge-os{RESET}
Verifies Obsidian meta vault (OBSIDIAN_ROOT / OBSIDIAN_META) and that
wiki-harvest and vault-paths symlinks exist under the configured LLM skills directories.""")
    elif subcmd == "":
        print(_usage())
    else:
        print(f"Unknown command: '{subcmd}'\n")
        print(_usage())
        sys.exit(1)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    cmd = args[0] if args else ""
    rest = args[1:]

    dispatch: dict = {
        "ls":           cmd_ls,
        "status":       cmd_status,
        "show":         cmd_show,
        "audit":        cmd_audit,
        "sync":         cmd_audit,
        "update":       cmd_update,
        "staging":      cmd_staging,
        "customize":    cmd_customize,
        "lint":         cmd_lint,
        "doctor":       cmd_doctor,
        "knowledge-os": cmd_knowledge_os,
        "memory-help":  cmd_memory_help,
        "git":          lambda a: cmd_git(a),
        "uninstall":    cmd_uninstall,
        "version":      cmd_version,
        "--version":    cmd_version,
        "config":       cmd_config,
        "help":         cmd_help,
        "--help":       cmd_help,
        "-h":           cmd_help,
    }

    if not cmd:
        print("Skill Forge — use metadata.status in each SKILL.md; run skillmanager help")
        sys.exit(1)

    handler = dispatch.get(cmd)
    if handler is None:
        die(f"Unknown command: '{cmd}'. Run 'skillmanager help' for usage.")

    handler(rest)


if __name__ == "__main__":
    main()
