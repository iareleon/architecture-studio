#!/usr/bin/env python3
"""check_skill_names.py — validates skill directory naming convention

Rules:
  - Skill names: lowercase letters, numbers, hyphens; must start with a letter
  - No -sme / -wf suffix (unified skills)
  - name: field in SKILL.md must equal the directory name exactly
  - name must not be a reserved state bucket (review, deactivated, etc.)
  - System skills may use -sys suffix (optional, rare)
  - Skills live under skills/<name>/; visibility is metadata.status in SKILL.md

Usage:
  python3 scripts/check_skill_names.py
  python3 scripts/check_skill_names.py --staged

Exit 0 = all valid, 1 = violations
"""

import os
import sys
import re
import subprocess
from pathlib import Path

IS_WINDOWS = sys.platform == "win32"

# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------

def _supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("TERM", "") != "dumb"

if _supports_color():
    RED    = "\033[31m"
    YELLOW = "\033[33m"
    GREEN  = "\033[32m"
    RESET  = "\033[0m"
else:
    RED = YELLOW = GREEN = RESET = ""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_RESERVED = {"review", "deactivated", "staging", "decommissioned", "sme", "workflow"}
_SKILL_NAME_RE = re.compile(r"^[a-z][a-z0-9-]+(-sys)?$")


def _is_skill_dir_name(name: str) -> bool:
    """Return True if name is a valid skill directory basename."""
    if name in _RESERVED:
        return False
    return bool(_SKILL_NAME_RE.match(name))


def _get_skills_dir() -> Path:
    env_val = os.environ.get("SKILLS_DIR", "")
    if env_val:
        return Path(env_val)
    # Derive from git root
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return Path(result.stdout.strip()) / "skills"
    return Path("skills")


def _get_staged_paths() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    return result.stdout.strip().splitlines() if result.returncode == 0 else []


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def check_skills_root_layout(skills_dir: Path) -> int:
    """Validate that skills/ root contains only valid entries."""
    violations = 0
    if not skills_dir.is_dir():
        return 0

    for item in skills_dir.iterdir():
        base = item.name
        if base.startswith("."):
            continue
        if item.is_file():
            if base != "README.md":
                print(f"{RED}[FAIL]{RESET}  unexpected file under skills/: {base}")
                violations += 1
            continue
        if _is_skill_dir_name(base):
            continue
        print(f"{RED}[FAIL]{RESET}  unexpected directory under skills/: {base}")
        violations += 1

    return violations


def check_skill_dir(dir_name: str, skills_dir: Path) -> int:
    """Validate a single skill directory name and its SKILL.md name: field."""
    violations = 0

    if not _is_skill_dir_name(dir_name):
        print(
            f"{RED}[FAIL]{RESET}  {dir_name} — invalid skill name "
            "(kebab-case; not a reserved state dir; optional -sys only)"
        )
        return 1

    skill_md_path = skills_dir / dir_name / "SKILL.md"
    if not skill_md_path.exists():
        # Check all subdirectories (for --staged paths that may not yet be on disk)
        matches = list(skills_dir.rglob(f"{dir_name}/SKILL.md"))
        skill_md_path = matches[0] if matches else None

    if skill_md_path and skill_md_path.exists():
        fm_name = ""
        for line in skill_md_path.read_text(encoding="utf-8").splitlines():
            if re.match(r"^name:\s*", line):
                fm_name = re.sub(r"^name:\s*", "", line).strip().strip("\"'")
                break

        if not fm_name:
            print(f"{RED}[FAIL]{RESET}  {dir_name} — SKILL.md missing name: field")
            violations += 1
        elif fm_name != dir_name:
            print(
                f"{RED}[FAIL]{RESET}  {dir_name} — SKILL.md name: \"{fm_name}\" "
                f"does not match directory name \"{dir_name}\""
            )
            violations += 1
        else:
            print(f"{GREEN}[OK]{RESET}    {dir_name}")
    else:
        print(f"{GREEN}[OK]{RESET}    {dir_name} (no SKILL.md to check)")

    return violations


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    staged_only = "--staged" in sys.argv

    skills_dir = _get_skills_dir()
    violations = 0

    if not staged_only and skills_dir.is_dir():
        violations += check_skills_root_layout(skills_dir)

    skill_dirs: list[str] = []

    if staged_only:
        seen: set[str] = set()
        for path in _get_staged_paths():
            m = re.match(r"^skills/([a-z][a-z0-9-]+(?:-sys)?)/", path)
            if not m:
                continue
            dir_name = m.group(1)
            if dir_name not in seen:
                seen.add(dir_name)
                skill_dirs.append(dir_name)
    else:
        if skills_dir.is_dir():
            for entry in sorted(skills_dir.iterdir()):
                if not entry.is_dir():
                    continue
                name = entry.name
                if name in _RESERVED:
                    continue
                if not (entry / "SKILL.md").exists():
                    continue
                skill_dirs.append(name)

    if not skill_dirs:
        sys.exit(0)

    for dir_name in skill_dirs:
        violations += check_skill_dir(dir_name, skills_dir)

    if violations > 0:
        print(f"\n{RED}{violations} naming violation(s) found.{RESET}")
        sys.exit(1)
    else:
        if not staged_only:
            print(f"{GREEN}[OK]{RESET}  All skill names comply with the naming standard.")
        sys.exit(0)


if __name__ == "__main__":
    main()
