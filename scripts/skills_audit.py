#!/usr/bin/env python3
"""skills_audit.py — content-quality audit for installed skills

Checks all active skills for:
  - Valid kebab-case directory naming (not reserved)
  - Frontmatter: name matches dir, description present, disable-model-invocation flag
  - Frontmatter: metadata.memory-file resolves if set
  - Lean structure: no contiguous prose block > 10 lines without a heading break
  - References section present when skill has lookup tables or inline specs
  - Legacy memory files (skills/<id>/memory/) without metadata.memory-file declared
  - Unreferenced persona files (persona/ present but no routing table row in SKILL.md)
  - last-updated frontmatter on persona files (warn if absent or stale > 90 days)
  - Deferred skill plans older than 30 days

Delegates symlink and state invariant issues to: skillmanager audit

Usage:
  python3 scripts/skills_audit.py [--skills-dir PATH] [--install-dir PATH]

  --skills-dir   Path to the skills source directory (default: ./skills relative to git root)
  --install-dir  Path to the installed SkillsLoom dir (default: ~/.skillsloom)

Exit 0 = clean or warnings only, 1 = failures found
"""

from __future__ import annotations

import os
import re
import sys
import datetime
from pathlib import Path
from typing import NamedTuple

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

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_RESERVED = {"review", "deactivated", "staging", "decommissioned", "sme", "workflow"}
_SKILL_NAME_RE = re.compile(r"^[a-z][a-z0-9-]+(-sys)?$")
_STALE_DAYS = 90
_DEFERRED_DAYS = 30
_MAX_PROSE_BLOCK = 10

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


class Finding(NamedTuple):
    skill: str
    level: str   # "FAIL" | "WARN" | "INFO"
    check: str
    detail: str


# ---------------------------------------------------------------------------
# YAML frontmatter helpers
# ---------------------------------------------------------------------------


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Extract flat key:value pairs from the first YAML frontmatter block."""
    fm: dict[str, str] = {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip("\"'")
        # nested metadata.key
        m2 = re.match(r"^\s{2}([\w-]+):\s*(.*)", line)
        if m2:
            fm[f"metadata.{m2.group(1)}"] = m2.group(2).strip().strip("\"'")
    return fm


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------


def _check_naming(skill_id: str) -> list[Finding]:
    if not _SKILL_NAME_RE.match(skill_id) or skill_id in _RESERVED:
        return [Finding(skill_id, "FAIL", "NAMING VIOLATION",
                        f"'{skill_id}' is not valid kebab-case or is a reserved name")]
    return []


def _check_frontmatter(skill_id: str, skill_md: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = skill_md.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)

    name_val = fm.get("name", "")
    if not name_val:
        findings.append(Finding(skill_id, "FAIL", "MISSING NAME", "name: field absent"))
    elif name_val != skill_id:
        findings.append(Finding(skill_id, "FAIL", "NAME MISMATCH",
                                f"name: '{name_val}' != dir '{skill_id}'"))

    if not fm.get("description", "").strip():
        findings.append(Finding(skill_id, "FAIL", "MISSING DESCRIPTION",
                                "description: field absent or empty"))

    if fm.get("metadata.disable-model-invocation", "").lower() != "true":
        findings.append(Finding(skill_id, "FAIL", "MISSING DMI FLAG",
                                "disable-model-invocation: true absent from frontmatter"))

    mem_file = fm.get("metadata.memory-file", "")
    if mem_file:
        resolved = skill_md.parent / mem_file
        if not resolved.exists():
            findings.append(Finding(skill_id, "FAIL", "BROKEN MEMORY-FILE REFERENCE",
                                    f"metadata.memory-file '{mem_file}' not found at {resolved}"))

    return findings


def _check_lean(skill_id: str, skill_md: Path) -> list[Finding]:
    """Flag any contiguous non-heading, non-code prose block exceeding _MAX_PROSE_BLOCK lines."""
    findings: list[Finding] = []
    lines = skill_md.read_text(encoding="utf-8").splitlines()

    in_frontmatter = False
    in_code_block = False
    current_heading = "(top of file)"
    block_len = 0

    for line in lines:
        stripped = line.strip()

        if stripped == "---":
            in_frontmatter = not in_frontmatter
            block_len = 0
            continue
        if in_frontmatter:
            continue

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            block_len = 0
            continue
        if in_code_block:
            continue

        if re.match(r"^#{1,6}\s", stripped):
            current_heading = stripped
            block_len = 0
            continue

        if stripped == "":
            block_len = 0
            continue

        # Skip table rows and list items from block counting — they are compact
        if stripped.startswith("|") or re.match(r"^[-*\d]", stripped):
            block_len = 0
            continue

        block_len += 1
        if block_len == _MAX_PROSE_BLOCK + 1:
            findings.append(Finding(skill_id, "WARN", "BLOATED SECTION",
                                    f"Prose block > {_MAX_PROSE_BLOCK} lines under '{current_heading}'"))

    return findings


def _check_references_section(skill_id: str, skill_md: Path) -> list[Finding]:
    """Warn if skill has routing tables but no ## References section."""
    text = skill_md.read_text(encoding="utf-8")
    has_table = bool(re.search(r"^\|", text, re.MULTILINE))
    has_references_heading = bool(re.search(r"^#{1,3}\s+References", text, re.MULTILINE))
    if has_table and not has_references_heading:
        return [Finding(skill_id, "WARN", "MISSING REFERENCES SECTION",
                        "Skill has lookup tables but no ## References heading")]
    return []


def _check_legacy_memory(skill_id: str, skill_dir: Path, skill_md: Path) -> list[Finding]:
    """Flag skills/<id>/memory/ directories where SKILL.md has no metadata.memory-file."""
    findings: list[Finding] = []
    memory_dir = skill_dir / "memory"
    if not memory_dir.is_dir():
        return findings
    # For the 'memory' skill itself the memory/ dir is its own workflow tree — skip
    if skill_id == "memory":
        return findings
    fm = _parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if not fm.get("metadata.memory-file"):
        findings.append(Finding(skill_id, "INFO", "LEGACY MEMORY FILE",
                                f"skills/{skill_id}/memory/ exists but metadata.memory-file not declared "
                                "— candidate to fold into SKILL.md or project CLAUDE.md"))
    return findings


def _check_persona_files(skill_id: str, skill_dir: Path, skill_md: Path) -> list[Finding]:
    """Check persona/ files for routing table rows and last-updated frontmatter."""
    findings: list[Finding] = []
    persona_dir = skill_dir / "persona"
    if not persona_dir.is_dir():
        return findings

    skill_text = skill_md.read_text(encoding="utf-8")
    today = datetime.date.today()

    for persona_file in sorted(persona_dir.glob("*.md")):
        fname = persona_file.name

        # Unreferenced persona check
        if fname not in skill_text:
            findings.append(Finding(skill_id, "WARN", "UNREFERENCED PERSONA",
                                    f"persona/{fname} not referenced in SKILL.md"))

        # last-updated check
        p_fm = _parse_frontmatter(persona_file.read_text(encoding="utf-8"))
        lu = p_fm.get("last-updated", "")
        if not lu:
            findings.append(Finding(skill_id, "WARN", "PERSONA MISSING LAST-UPDATED",
                                    f"persona/{fname} has no last-updated frontmatter field (I-6)"))
        else:
            try:
                lu_date = datetime.date.fromisoformat(lu)
                age = (today - lu_date).days
                if age > _STALE_DAYS:
                    findings.append(Finding(skill_id, "WARN", "STALE PERSONA",
                                            f"persona/{fname} last-updated {lu} ({age} days ago)"))
            except ValueError:
                findings.append(Finding(skill_id, "WARN", "INVALID LAST-UPDATED",
                                        f"persona/{fname} last-updated value '{lu}' is not ISO-8601"))

    return findings


def _check_deferred_plans(skills_dir: Path) -> list[Finding]:
    """Flag deferred skill plans older than _DEFERRED_DAYS days."""
    findings: list[Finding] = []
    deferred_dir = skills_dir / "skill-manager" / "references" / "deferred-skill-plans"
    if not deferred_dir.is_dir():
        return findings
    today = datetime.date.today()
    for plan in sorted(deferred_dir.glob("*.md")):
        if plan.name.lower() == "readme.md":
            continue
        fm = _parse_frontmatter(plan.read_text(encoding="utf-8"))
        deferred_on = fm.get("deferred-on", "")
        if not deferred_on:
            findings.append(Finding("skill-manager", "INFO", "DEFERRED SKILL OVERDUE",
                                    f"{plan.name} — no deferred-on date found"))
            continue
        try:
            d = datetime.date.fromisoformat(deferred_on)
            age = (today - d).days
            if age > _DEFERRED_DAYS:
                findings.append(Finding("skill-manager", "INFO", "DEFERRED SKILL OVERDUE",
                                        f"{plan.name} deferred {age} days ago (>{_DEFERRED_DAYS})"))
        except ValueError:
            findings.append(Finding("skill-manager", "INFO", "DEFERRED SKILL OVERDUE",
                                    f"{plan.name} — deferred-on value '{deferred_on}' is not ISO-8601"))
    return findings


# ---------------------------------------------------------------------------
# Main audit runner
# ---------------------------------------------------------------------------


def _discover_skills(skills_dir: Path) -> list[Path]:
    if not skills_dir.is_dir():
        return []
    result = []
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if entry.name in _RESERVED:
            continue
        if not (entry / "SKILL.md").exists():
            continue
        result.append(entry)
    return result


def _resolve_skills_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser()
    # Try install dir first, fall back to repo
    install = Path.home() / ".skillsloom" / "skills"
    if install.is_dir():
        return install
    legacy = Path.home() / ".skillmanager" / "skills"
    if legacy.is_dir():
        return legacy
    # Fall back to repo-relative
    import subprocess
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                       capture_output=True, text=True)
    if r.returncode == 0:
        return Path(r.stdout.strip()) / "skills"
    return Path("skills")


def _print_report(all_findings: list[Finding]) -> int:
    """Print the findings table. Returns number of FAIL-level findings."""
    if not all_findings:
        print(f"\n{GREEN}[OK]{RESET}  All skills passed the content audit.\n")
        return 0

    col_skill = max(len(f.skill) for f in all_findings)
    col_check = max(len(f.check) for f in all_findings)

    header = (f"{'Skill':<{col_skill}}  {'Check':<{col_check}}  Level   Detail")
    print(f"\n{BOLD}{header}{RESET}")
    print("-" * len(header))

    failures = 0
    for f in sorted(all_findings, key=lambda x: (x.skill, x.level, x.check)):
        if f.level == "FAIL":
            color, failures = RED, failures + 1
        elif f.level == "WARN":
            color = YELLOW
        else:
            color = CYAN
        print(f"{f.skill:<{col_skill}}  {f.check:<{col_check}}  "
              f"{color}{f.level:<7}{RESET}  {f.detail}")

    print()
    counts = {"FAIL": 0, "WARN": 0, "INFO": 0}
    for f in all_findings:
        counts[f.level] += 1

    parts = []
    if counts["FAIL"]:
        parts.append(f"{RED}{counts['FAIL']} failure(s){RESET}")
    if counts["WARN"]:
        parts.append(f"{YELLOW}{counts['WARN']} warning(s){RESET}")
    if counts["INFO"]:
        parts.append(f"{CYAN}{counts['INFO']} info item(s){RESET}")
    print("Summary: " + ", ".join(parts))
    print(f"\nFor symlink/state issues run: {BOLD}skillmanager audit{RESET}\n")

    return failures


def main() -> None:
    args = sys.argv[1:]

    skills_dir_arg = None
    i = 0
    while i < len(args):
        if args[i] == "--skills-dir" and i + 1 < len(args):
            skills_dir_arg = args[i + 1]
            i += 2
        elif args[i].startswith("--skills-dir="):
            skills_dir_arg = args[i].split("=", 1)[1]
            i += 1
        else:
            i += 1

    skills_dir = _resolve_skills_dir(skills_dir_arg)

    if not skills_dir.is_dir():
        print(f"{RED}[ERROR]{RESET} skills dir not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"{CYAN}[INFO]{RESET}  Auditing skills in: {skills_dir}")

    skill_dirs = _discover_skills(skills_dir)
    if not skill_dirs:
        print(f"{YELLOW}[WARN]{RESET}  No skills found.")
        sys.exit(0)

    all_findings: list[Finding] = []

    for skill_dir in skill_dirs:
        skill_id = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        all_findings += _check_naming(skill_id)
        all_findings += _check_frontmatter(skill_id, skill_md)
        all_findings += _check_lean(skill_id, skill_md)
        all_findings += _check_references_section(skill_id, skill_md)
        all_findings += _check_legacy_memory(skill_id, skill_dir, skill_md)
        all_findings += _check_persona_files(skill_id, skill_dir, skill_md)

    all_findings += _check_deferred_plans(skills_dir)

    failures = _print_report(all_findings)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
