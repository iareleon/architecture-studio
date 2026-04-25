#!/usr/bin/env python3
"""install.py — idempotent installer for Skill Forge

Safe to run multiple times. Never overwrites existing skill data.
Reads config from ~/.skillmanager/config.yaml if it already exists.

Usage: python3 scripts/install.py
Override defaults: SKILLMANAGER_DIR=/custom/path python3 scripts/install.py
"""

import os
import sys
import re
import shutil
import hashlib
import datetime
import subprocess
import platform
from pathlib import Path

IS_WINDOWS = sys.platform == "win32"
_HOME = Path.home()

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


def info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET}  {msg}")

def ok(msg: str) -> None:
    print(f"{GREEN}[OK]{RESET}    {msg}")

def warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET}  {msg}", file=sys.stderr)

def die(msg: str) -> None:
    print(f"{RED}[ERROR]{RESET} {msg}", file=sys.stderr)
    sys.exit(1)

def header(msg: str) -> None:
    print(f"\n{BOLD}{msg}{RESET}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        h.update(path.read_bytes())
        return h.hexdigest()
    except OSError:
        return ""


def detect_tool(tool: str) -> bool:
    found = shutil.which(tool)
    if found:
        ok(f"Found: {tool} ({found})")
        return True
    warn(f"Not found: {tool} — skills requiring this tool will not be activated")
    return False


def _safe_symlink(src: Path, dst: Path) -> bool:
    try:
        if dst.is_symlink():
            dst.unlink()
        os.symlink(src, dst)
        return True
    except OSError as exc:
        if IS_WINDOWS and hasattr(exc, "winerror") and exc.winerror == 1314:
            warn(
                f"Symlink creation requires Developer Mode or admin rights on Windows: {dst}\n"
                "  Enable: Settings → System → For Developers → Developer Mode"
            )
        else:
            warn(f"Failed to create symlink: {exc}")
        return False


# ---------------------------------------------------------------------------
# Platform-specific path defaults
# ---------------------------------------------------------------------------

def _get_default_install_dir() -> Path:
    return _HOME / ".skillmanager"


def _get_default_bin_dir() -> Path:
    if IS_WINDOWS:
        local_appdata = os.environ.get("LOCALAPPDATA", str(_HOME / "AppData" / "Local"))
        return Path(local_appdata) / "Programs" / "skillmanager"
    return _HOME / ".local" / "bin"


def _get_llm_skills_dir(llm: str) -> Path:
    """Return default skills dir for a given LLM."""
    return _HOME / f".{llm}" / "skills"


def _get_llm_context_file(llm: str) -> Path:
    ext = "CLAUDE.md" if llm == "claude" else f"{llm.upper()}.md"
    return _HOME / f".{llm}" / ext


# ---------------------------------------------------------------------------
# Run audit via skillmanager binary or script
# ---------------------------------------------------------------------------

def _run_audit(cli_binary: Path, skillmanager_dir: Path) -> None:
    env = {**os.environ, "SKILLMANAGER_DIR": str(skillmanager_dir)}
    result = subprocess.run([sys.executable, str(cli_binary), "audit"], env=env)
    if result.returncode != 0:
        warn("skillmanager audit reported issues. Run: skillmanager doctor && skillmanager audit")


# ---------------------------------------------------------------------------
# Main installer
# ---------------------------------------------------------------------------

def main() -> None:
    # Resolve paths from script location
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    repo_skills_dir = repo_root / "skills"

    header("Skill Forge Installer")
    print("\nThis installer will set up Skill Forge on your system.")
    print("Press Enter to accept defaults shown in [brackets].\n")

    # -----------------------------------------------------------------------
    # Step 1 — Interactive configuration
    # -----------------------------------------------------------------------

    # Install directory
    env_dir = os.environ.get("SKILLMANAGER_DIR", "")
    if env_dir:
        info(f"Using SKILLMANAGER_DIR override: {env_dir}")
        skillmanager_dir = Path(env_dir.replace("~", str(_HOME)))
    else:
        default_dir = _get_default_install_dir()
        user_input = input(f"Where should Skill Forge assets live? [{default_dir}]: ").strip()
        skillmanager_dir = Path((user_input or str(default_dir)).replace("~", str(_HOME)))

    # Reject git repositories as install targets
    while (skillmanager_dir / ".git").is_dir():
        warn(f"'{skillmanager_dir}' is a git repository. Skill Forge must be installed outside any cloned repo.")
        user_input = input(f"Choose a different directory [{_get_default_install_dir()}]: ").strip()
        skillmanager_dir = Path((user_input or str(_get_default_install_dir())).replace("~", str(_HOME)))

    skills_dir = skillmanager_dir / "skills"
    config_file = _HOME / ".skillmanager" / "config.yaml"
    bin_dir = _get_default_bin_dir()

    # LLM targets
    print("\nWhich LLMs do you use? (space-separated, e.g. 'claude gemini')")
    print("Available: claude, gemini [claude]: ", end="", flush=True)
    user_llms = input().strip() or "claude"

    selected_llms = []
    for llm in user_llms.split():
        if llm in ("claude", "gemini"):
            selected_llms.append(llm)
        else:
            warn(f"Unknown LLM '{llm}' — skipping. Supported: claude, gemini")
    if not selected_llms:
        die("No valid LLM targets selected.")

    # Email (optional)
    user_email = input("\nEmail address for skill proposal notifications (optional, press Enter to skip): ").strip()

    # System skills mode
    print("\nSystem skills (skill detection, memory management) can run automatically")
    print("every session, or be invoked manually when needed.\n")
    print("  [A] Always-on  — rules embedded in model.md, active after every /clear")
    print("  [M] Manual     — invoke /skill-manager or /memory when you need them\n")
    print("Recommendation: Manual keeps initial memory small.")
    sys_choice = input("Choice [M]: ").strip().upper() or "M"
    system_skills_mode = "always-on" if sys_choice in ("A", "ALWAYS", "ALWAYS-ON") else "manual"
    ok(f"System skills mode: {system_skills_mode}")

    # -----------------------------------------------------------------------
    # Step 2 — Tool detection
    # -----------------------------------------------------------------------
    header("Step 2: Detecting required tools")

    has_git       = detect_tool("git")
    has_gh        = detect_tool("gh")
    has_glab      = detect_tool("glab")
    has_gcloud    = detect_tool("gcloud")
    has_terraform = detect_tool("terraform")

    # -----------------------------------------------------------------------
    # Step 3 — Create directory structure
    # -----------------------------------------------------------------------
    header("Step 3: Creating directory structure")

    for d in [skillmanager_dir, skills_dir, bin_dir]:
        if d.is_dir():
            info(f"Already exists: {d}")
        else:
            d.mkdir(parents=True, exist_ok=True)
            ok(f"Created: {d}")

    for llm in selected_llms:
        llm_dir = _get_llm_skills_dir(llm)
        if llm_dir.is_dir():
            info(f"Already exists: {llm_dir}")
        else:
            llm_dir.mkdir(parents=True, exist_ok=True)
            ok(f"Created: {llm_dir}")

    # -----------------------------------------------------------------------
    # Step 4 — Write config.yaml
    # -----------------------------------------------------------------------
    header("Step 4: Writing config.yaml")

    config_file.parent.mkdir(parents=True, exist_ok=True)

    llm_targets_yaml = ""
    for llm in selected_llms:
        skills_path = _get_llm_skills_dir(llm)
        context_path = _get_llm_context_file(llm)
        llm_targets_yaml += (
            f"  - name: {llm}\n"
            f"    skills_dir: {skills_path}\n"
            f"    context_file: {context_path}\n"
        )

    config_content = (
        "# Skill Forge configuration — generated by install.py\n"
        "# Edit this file to add or remove LLM targets.\n"
        'version: "1"\n'
        f"install_dir: {skillmanager_dir}\n"
        "user:\n"
        f'  email: "{user_email}"\n'
        f"system_skills_mode: {system_skills_mode}\n"
        "llm_targets:\n"
        f"{llm_targets_yaml}"
        "tools:\n"
        f"  git: {str(has_git).lower()}\n"
        f"  gh: {str(has_gh).lower()}\n"
        f"  glab: {str(has_glab).lower()}\n"
        f"  gcloud: {str(has_gcloud).lower()}\n"
        f"  terraform: {str(has_terraform).lower()}\n"
    )
    config_file.write_text(config_content, encoding="utf-8")
    ok(f"Config written: {config_file}")

    # -----------------------------------------------------------------------
    # Step 5 — Copy starter skills (never overwrite existing)
    # -----------------------------------------------------------------------
    header("Step 5: Installing starter skills")

    _RESERVED = {"review", "deactivated", "staging", "decommissioned", "sme", "workflow"}

    if not repo_skills_dir.is_dir():
        warn(f"No skills directory at {repo_skills_dir} — skipping skill copy.")
    else:
        for skill_dir in sorted(repo_skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            local_name = skill_dir.name
            if local_name in _RESERVED:
                continue
            if not (skill_dir / "SKILL.md").exists():
                continue
            target = skills_dir / local_name
            if target.is_dir():
                info(f"Already present, skipping: {local_name}")
                continue
            shutil.copytree(skill_dir, target)
            ok(f"Installed: {local_name} → {target}")

    # -----------------------------------------------------------------------
    # Step 6 — Persona model.md
    # -----------------------------------------------------------------------
    header("Step 6: Setting up persona file")

    model_file = skillmanager_dir / "model.md"
    persona_src = repo_root / "skills" / "skill-manager" / "templates" / "persona" / "model.md"
    persona_sys_src = repo_root / "skills" / "skill-manager" / "templates" / "persona" / f"system-skills-{system_skills_mode}.md"

    if model_file.exists():
        info(f"Persona file already exists: {model_file}")
    else:
        print(f"\nSkill Forge uses a personal persona file to set your AI assistant identity.")
        print("It is saved locally and never committed to Git.\n")
        create_model = input(f"Create persona file at {model_file}? [Y/n]: ").strip() or "Y"
        if create_model.upper() == "Y":
            if persona_src.exists():
                shutil.copy2(persona_src, model_file)
                if persona_sys_src.exists():
                    model_file.open("a", encoding="utf-8").write(
                        persona_sys_src.read_text(encoding="utf-8")
                    )
                ok(f"Created persona template: {model_file}")
                info("Edit this file to set your personal AI assistant persona.")
            else:
                info(f"Persona template not found at {persona_src} — skipping.")
        else:
            info("Skipped persona file creation.")

    # Reference model.md from each LLM's context file
    if model_file.exists():
        model_import = f"@{model_file}"
        for llm in selected_llms:
            ctx_file = _get_llm_context_file(llm)
            if not ctx_file.exists():
                info(f"{llm}: context file not found ({ctx_file}) — skipping model.md reference")
                continue
            text = ctx_file.read_text(encoding="utf-8")
            if model_import in text:
                info(f"{llm}: model.md already referenced in {ctx_file}")
            else:
                ctx_file.open("a", encoding="utf-8").write(f"\n# Skill Forge persona\n{model_import}\n")
                ok(f"{llm}: added model.md reference to {ctx_file}")

    # -----------------------------------------------------------------------
    # Step 7 — Install CLI binary
    # -----------------------------------------------------------------------
    header("Step 7: Installing Skill Forge CLI")

    cli_src = script_dir / "skillmanager.py"
    if not cli_src.exists():
        die(f"CLI script not found: {cli_src}")

    cli_binary = bin_dir / "skillmanager"
    shutil.copy2(cli_src, cli_binary)

    if not IS_WINDOWS:
        os.chmod(cli_binary, 0o755)
        # Ensure shebang is executable — inject if missing
        text = cli_binary.read_text(encoding="utf-8")
        if not text.startswith("#!/usr/bin/env python3"):
            cli_binary.write_text("#!/usr/bin/env python3\n" + text, encoding="utf-8")
    else:
        # On Windows, create a .cmd wrapper so `skillmanager` works in cmd.exe
        cmd_wrapper = bin_dir / "skillmanager.cmd"
        cmd_wrapper.write_text(
            f'@echo off\npython3 "{cli_binary}" %*\n', encoding="utf-8"
        )
        ok(f"Created Windows wrapper: {cmd_wrapper}")

    ok(f"Installed CLI: {cli_binary}")

    # -----------------------------------------------------------------------
    # Step 8 — Sync LLM symlinks
    # -----------------------------------------------------------------------
    header("Step 8: Syncing LLM symlinks (skillmanager audit)")
    _run_audit(cli_binary, skillmanager_dir)

    # -----------------------------------------------------------------------
    # Step 9 — Ensure bin dir is in PATH
    # -----------------------------------------------------------------------
    header("Step 9: Configuring PATH")

    if IS_WINDOWS:
        info(
            f"On Windows, add '{bin_dir}' to your PATH via:\n"
            "  System Properties → Advanced → Environment Variables → PATH"
        )
    else:
        path_line   = 'export PATH="$HOME/.local/bin:$PATH"'
        path_comment = "# Added by Skill Forge install"
        for rc_name in (".bashrc", ".zshrc"):
            rc_file = _HOME / rc_name
            if not rc_file.exists():
                info(f"Not found, skipping: {rc_file}")
                continue
            text = rc_file.read_text(encoding="utf-8")
            if path_line in text:
                info(f"PATH already configured in {rc_file}")
            else:
                rc_file.open("a", encoding="utf-8").write(f"\n{path_comment}\n{path_line}\n")
                ok(f"Appended PATH export to {rc_file}")

    # -----------------------------------------------------------------------
    # Step 10 — Install git hooks
    # -----------------------------------------------------------------------
    header("Step 10: Installing git hooks")

    git_hooks_dir = repo_root / ".git" / "hooks"
    hooks_src_dir = script_dir / "hooks"

    if not git_hooks_dir.is_dir():
        warn("No .git/hooks directory found — skipping hook installation.")
    elif hooks_src_dir.is_dir():
        for hook_src in sorted(hooks_src_dir.iterdir()):
            if not hook_src.is_file():
                continue
            hook_dest = git_hooks_dir / hook_src.name
            if hook_dest.exists() and not hook_dest.is_symlink():
                warn(f"Hook exists (not a symlink): {hook_dest} — skipping. Back it up and re-run to install.")
            else:
                shutil.copy2(hook_src, hook_dest)
                if not IS_WINDOWS:
                    os.chmod(hook_dest, 0o755)
                ok(f"Installed hook: {hook_src.name}")

    # -----------------------------------------------------------------------
    # Step 11 — Generate install checksums
    # -----------------------------------------------------------------------
    header("Step 11: Recording install checksums")

    checksums_file = skillmanager_dir / ".checksums"
    install_version_file = skillmanager_dir / ".install-version"

    checksum_lines = []
    for f in sorted(skills_dir.rglob("*")):
        if not f.is_file():
            continue
        h = sha256_file(f)
        if h:
            rel = f.relative_to(skillmanager_dir)
            checksum_lines.append(f"{h}  {rel}")

    checksums_file.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    ok(f"Checksums written: {checksums_file}")

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    install_version_file.write_text(timestamp + "\n", encoding="utf-8")
    ok(f"Install timestamp recorded: {timestamp}")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    header("Installation Complete")

    print(f"\n  {'Install directory:':<28} {skillmanager_dir}")
    print(f"  {'Config file:':<28} {config_file}")
    print(f"  {'LLM targets:':<28} {', '.join(selected_llms)}")
    print(f"  {'CLI binary:':<28} {cli_binary}")

    print(f"\n{BOLD}Next steps:{RESET}")
    if IS_WINDOWS:
        print(f"  1. Add to PATH:               {bin_dir}")
    else:
        print("  1. Reload your shell:         source ~/.zshrc  (or ~/.bashrc)")
    print(f"  2. Edit your persona:         {model_file}")
    print(f"  3. Skill main brain:          {skillmanager_dir}/skills/<name>/SKILL.md")
    print("  4. Verify environment:        skillmanager doctor")
    print("  5. List installed skills:     skillmanager ls")
    print(f"\n{BOLD}Safe test (no live data touched):{RESET}")
    print(f"  SKILLMANAGER_DIR=/tmp/sf-test python3 {script_dir}/install.py")
    print()


if __name__ == "__main__":
    main()
