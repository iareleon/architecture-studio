#!/usr/bin/env python3
"""test_env_setup.py — scaffold an isolated SkillsLoom test environment

Creates a temporary install directory that mirrors the real install structure
without touching production skill directories or LLM context files.

LLM test symlinks are created at {LLM_DIR}/skills/<name> only for skills
that have no existing production symlink at that path. Each created symlink
is recorded in $TMP_SKILLMANAGER_DIR/.test-manifest for clean teardown.

IMPORTANT: SKILLSLOOM_DIR is production-only. This script manages
TMP_SKILLMANAGER_DIR exclusively. Never set SKILLSLOOM_DIR manually for testing.

Usage:
  python3 scripts/test_env_setup.py

Teardown:
  python3 scripts/test_env_teardown.py
"""

import os
import sys
import subprocess
import shutil
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
    CYAN   = "\033[36m"
    RESET  = "\033[0m"
else:
    BOLD = GREEN = YELLOW = CYAN = RESET = ""


def info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET}  {msg}")

def ok(msg: str) -> None:
    print(f"{GREEN}[OK]{RESET}    {msg}")

def warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET}  {msg}", file=sys.stderr)

def header(msg: str) -> None:
    print(f"\n{BOLD}{msg}{RESET}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_RESERVED = {"review", "deactivated", "staging", "decommissioned", "sme", "workflow"}


def _production_config_file() -> Path:
    """Match skillmanager.py: ~/.skillsloom/config.yaml first, then legacy ~/.skillmanager."""
    primary = _HOME / ".skillsloom" / "config.yaml"
    if primary.is_file():
        return primary
    legacy = _HOME / ".skillmanager" / "config.yaml"
    if legacy.is_file():
        return legacy
    return primary


def _configured_llm_dirs() -> list[Path]:
    """Resolve configured LLM skill dirs from config.yaml."""
    config_file = _production_config_file()
    dirs = []
    if config_file.exists():
        for line in config_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("skills_dir:"):
                val = stripped.split(":", 1)[1].strip().strip("\"'")
                if val:
                    dirs.append(Path(val.replace("~", str(_HOME))))
    if not dirs:
        dirs.append(_HOME / ".claude" / "skills")
    return dirs


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
            warn(f"Failed to create symlink {dst} → {src}: {exc}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    repo_skills_dir = repo_root / "skills"

    tmp_skillmanager_dir = repo_root / ".tmp-skillmanager"
    tmp_skills_dir = tmp_skillmanager_dir / "skills"
    test_manifest = tmp_skillmanager_dir / ".test-manifest"

    header("Test Environment Setup")
    print(f"\nTMP_SKILLMANAGER_DIR = {tmp_skillmanager_dir}\n")

    if tmp_skillmanager_dir.is_dir():
        warn(f"Test environment already exists at {tmp_skillmanager_dir}")
        warn("Run scripts/test_env_teardown.py first, or proceed to reuse it.")

    # -----------------------------------------------------------------------
    # Step 1 — Create tmp install directory structure
    # -----------------------------------------------------------------------
    for subdir in ("deactivated", "review", "staging", "decommissioned"):
        (tmp_skills_dir / subdir).mkdir(parents=True, exist_ok=True)

    test_manifest.touch()
    ok(f"Created directory structure: {tmp_skills_dir}")

    # -----------------------------------------------------------------------
    # Step 2 — Copy skills from repo into tmp (never overwrite)
    # -----------------------------------------------------------------------
    header("Copying skills to test environment")

    if repo_skills_dir.is_dir():
        for src_dir in sorted(repo_skills_dir.iterdir()):
            if not src_dir.is_dir():
                continue
            skill_name = src_dir.name
            if skill_name in _RESERVED:
                continue
            if not (src_dir / "SKILL.md").exists():
                continue
            target = tmp_skills_dir / skill_name
            if target.is_dir():
                info(f"Already present, skipping: {skill_name}")
            else:
                shutil.copytree(src_dir, target)
                ok(f"Copied: {skill_name}")
    else:
        warn(f"No skills directory found at {repo_skills_dir} — skipping copy.")

    # -----------------------------------------------------------------------
    # Step 3 — Create LLM test symlinks
    # -----------------------------------------------------------------------
    header("Creating LLM test symlinks")

    manifest_entries: list[str] = []
    existing_entries = set(test_manifest.read_text(encoding="utf-8").splitlines()) if test_manifest.exists() else set()

    for llm_skills_dir in _configured_llm_dirs():
        if not llm_skills_dir.is_dir():
            info(f"LLM skills dir not found, skipping: {llm_skills_dir}")
            continue
        for skill_dir in sorted(tmp_skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_name = skill_dir.name
            if skill_name in _RESERVED:
                continue
            if not (skill_dir / "SKILL.md").exists():
                continue

            link = llm_skills_dir / skill_name
            if link.is_symlink() or link.exists():
                info(f"Production symlink exists — skipping test link: {skill_name}")
                continue

            if _safe_symlink(skill_dir, link):
                link_str = str(link)
                if link_str not in existing_entries:
                    manifest_entries.append(link_str)
                ok(f"Linked: {link} → {skill_dir}")

    # Append new entries to manifest
    if manifest_entries:
        with test_manifest.open("a", encoding="utf-8") as f:
            for entry in manifest_entries:
                f.write(entry + "\n")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    header("Test Environment Ready")
    print()
    print(f"  {'Test install dir:':<30} {tmp_skillmanager_dir}")
    print(f"  {'Test skills dir:':<30} {tmp_skills_dir}")
    print(f"  {'Symlink manifest:':<30} {test_manifest}")
    print()
    print(f"{BOLD}Test skills are visible to your LLM at: {{LLM_DIR}}/skills/<name>{RESET}")
    print("Production skills are unchanged.")
    print()
    print(f"{BOLD}IMPORTANT:{RESET} SKILLSLOOM_DIR is production-only.")
    print("This script manages TMP_SKILLMANAGER_DIR only.")
    print("Never set SKILLSLOOM_DIR manually for testing.")
    print(f"\nTo set the test variable in your shell:")
    if IS_WINDOWS:
        print(f'  set TMP_SKILLMANAGER_DIR="{tmp_skillmanager_dir}"')
    else:
        print(f'  export TMP_SKILLMANAGER_DIR="{tmp_skillmanager_dir}"')
    print(f"\nTo tear down: python3 {script_dir}/test_env_teardown.py\n")


if __name__ == "__main__":
    main()
