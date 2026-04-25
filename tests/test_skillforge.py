"""test_skillforge.py — pytest tests for the Skill Forge CLI (skillmanager.py)

Prerequisites:
  pip install pytest

Run:
  pytest tests/test_skillforge.py -v
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
SKILLMANAGER = str(SCRIPTS_DIR / "skillmanager.py")
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

ACTIVE_SKILL_MD = textwrap.dedent("""\
    ---
    name: test-skill
    description: Minimal test fixture. Do not activate in production.
    metadata:
      version: "1.0"
      disable-model-invocation: true
    ---

    # Test Skill
    """)


@pytest.fixture()
def env(tmp_path: Path):
    """Create an isolated test environment for each test."""
    skillmanager_dir = tmp_path / "skillmanager"
    skills_dir = skillmanager_dir / "skills"
    claude_skills = tmp_path / "claude-skills"
    gemini_skills = tmp_path / "gemini-skills"
    claude_staging = tmp_path / "claude-skills-staging"
    gemini_staging = tmp_path / "gemini-skills-staging"

    for d in [skills_dir, claude_skills, gemini_skills, claude_staging, gemini_staging]:
        d.mkdir(parents=True)

    # Copy fixture skills
    if FIXTURES_DIR.is_dir():
        for entry in FIXTURES_DIR.iterdir():
            if entry.is_dir() and (entry / "SKILL.md").exists():
                import shutil
                shutil.copytree(entry, skills_dir / entry.name)
            elif entry.is_file() and entry.suffix == ".md":
                # skill md directly in fixtures
                pass

    # Minimal config.yaml so skillmanager doesn't complain
    config = skillmanager_dir / "config.yaml"
    config.write_text(
        f'version: "1"\n'
        f"install_dir: {skillmanager_dir}\n"
        "llm_targets:\n"
        f"  - name: claude\n"
        f"    skills_dir: {claude_skills}\n"
        f"    context_file: {tmp_path}/claude/CLAUDE.md\n",
        encoding="utf-8",
    )

    return {
        "skillmanager_dir": skillmanager_dir,
        "skills_dir": skills_dir,
        "claude_skills": claude_skills,
        "gemini_skills": gemini_skills,
        "claude_staging": claude_staging,
        "gemini_staging": gemini_staging,
        "env": {
            "SKILLMANAGER_DIR": str(skillmanager_dir),
            "CLAUDE_SKILLS_DIR": str(claude_skills),
            "GEMINI_SKILLS_DIR": str(gemini_skills),
            "CLAUDE_SKILLS_STAGING_DIR": str(claude_staging),
            "GEMINI_SKILLS_STAGING_DIR": str(gemini_staging),
        },
    }


def run_skillmanager(args: list[str], env_ctx: dict, input_text: str = "") -> subprocess.CompletedProcess:
    """Run skillmanager.py with the given args and environment."""
    full_env = {**os.environ, **env_ctx["env"]}
    return subprocess.run(
        [sys.executable, SKILLMANAGER] + args,
        capture_output=True,
        text=True,
        input=input_text,
        env=full_env,
    )


def add_test_skill(skills_dir: Path, name: str = "test-skill", status: str = "") -> Path:
    """Add a skill to the test skills directory."""
    skill_dir = skills_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    status_line = f"  status: {status}\n" if status else ""
    skill_md = (
        f"---\n"
        f"name: {name}\n"
        f"description: Minimal test fixture. Do not activate in production.\n"
        f"metadata:\n"
        f"  version: \"1.0\"\n"
        f"{status_line}"
        f"  disable-model-invocation: true\n"
        f"---\n\n"
        f"# {name.replace('-', ' ').title()}\n"
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    return skill_dir


# ---------------------------------------------------------------------------
# version
# ---------------------------------------------------------------------------

def test_version_prints_version_string(env):
    result = run_skillmanager(["version"], env)
    assert result.returncode == 0
    assert "skillmanager" in result.stdout


# ---------------------------------------------------------------------------
# help
# ---------------------------------------------------------------------------

def test_help_exits_0_and_prints_usage(env):
    result = run_skillmanager(["help"], env)
    assert result.returncode == 0
    assert "USAGE" in result.stdout


def test_help_with_unknown_command_exits_nonzero(env):
    result = run_skillmanager(["help", "nonexistent-command"], env)
    assert result.returncode != 0


def test_no_arguments_prints_hint_and_exits_nonzero(env):
    result = run_skillmanager([], env)
    assert result.returncode != 0
    assert "skillmanager help" in result.stdout or "skillmanager help" in result.stderr


# ---------------------------------------------------------------------------
# ls
# ---------------------------------------------------------------------------

def test_ls_lists_the_fixture_skill(env):
    add_test_skill(env["skills_dir"])
    result = run_skillmanager(["ls"], env)
    assert result.returncode == 0
    assert "test-skill" in result.stdout


# ---------------------------------------------------------------------------
# audit / metadata.status
# ---------------------------------------------------------------------------

def test_audit_creates_symlinks_for_active_skill(env):
    add_test_skill(env["skills_dir"])
    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    link = env["claude_skills"] / "test-skill"
    assert link.is_symlink()


def test_audit_deactivated_removes_symlinks(env):
    add_test_skill(env["skills_dir"], status="deactivated")
    # Pre-create a stale symlink
    stale = env["claude_skills"] / "test-skill"
    stale.symlink_to(env["skills_dir"] / "test-skill")
    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    assert not stale.is_symlink()


def test_show_on_unknown_skill_exits_nonzero(env):
    result = run_skillmanager(["show", "no-such-skill"], env)
    assert result.returncode != 0


# ---------------------------------------------------------------------------
# audit
# ---------------------------------------------------------------------------

def test_audit_passes_with_clean_environment(env):
    add_test_skill(env["skills_dir"])
    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0


def test_audit_detects_and_fixes_missing_symlink(env):
    add_test_skill(env["skills_dir"])
    run_skillmanager(["audit"], env)
    link = env["claude_skills"] / "test-skill"
    assert link.is_symlink()
    link.unlink()
    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    assert link.is_symlink()


def test_sync_is_alias_for_audit(env):
    add_test_skill(env["skills_dir"])
    result = run_skillmanager(["sync"], env)
    assert result.returncode == 0
    link = env["claude_skills"] / "test-skill"
    assert link.is_symlink()


# ---------------------------------------------------------------------------
# lint
# ---------------------------------------------------------------------------

def test_lint_passes_on_valid_skill_md(env):
    skill_dir = add_test_skill(env["skills_dir"])
    result = run_skillmanager(["lint", str(skill_dir / "SKILL.md")], env)
    assert result.returncode == 0


# ---------------------------------------------------------------------------
# doctor
# ---------------------------------------------------------------------------

def test_doctor_exits_0_and_shows_environment_info(env):
    result = run_skillmanager(["doctor"], env)
    assert result.returncode == 0
    assert "Doctor" in result.stdout


# ---------------------------------------------------------------------------
# config
# ---------------------------------------------------------------------------

def test_config_prints_config_file_contents(env):
    result = run_skillmanager(["config"], env)
    assert result.returncode == 0
    assert "install_dir" in result.stdout


# ---------------------------------------------------------------------------
# unknown command
# ---------------------------------------------------------------------------

def test_unknown_command_exits_nonzero_with_helpful_message(env):
    result = run_skillmanager(["notacommand"], env)
    assert result.returncode != 0
    assert "Unknown command" in result.stderr


# ---------------------------------------------------------------------------
# staging (metadata.status)
# ---------------------------------------------------------------------------

def test_staging_status_creates_symlinks_in_staging_not_production(env):
    add_test_skill(env["skills_dir"], status="staging")
    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    staging_link = env["claude_staging"] / "test-skill"
    prod_link = env["claude_skills"] / "test-skill"
    assert staging_link.is_symlink()
    assert not prod_link.is_symlink()


def test_switching_to_review_removes_staging_symlinks(env):
    # Start as staging
    add_test_skill(env["skills_dir"], status="staging")
    run_skillmanager(["audit"], env)
    staging_link = env["claude_staging"] / "test-skill"
    assert staging_link.is_symlink()

    # Switch to review
    skill_md = env["skills_dir"] / "test-skill" / "SKILL.md"
    skill_md.write_text(
        "---\n"
        "name: test-skill\n"
        "description: review test\n"
        "metadata:\n"
        '  version: "1.0"\n'
        "  status: review\n"
        "  disable-model-invocation: true\n"
        "---\n\n# Test Skill\n",
        encoding="utf-8",
    )
    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    assert not staging_link.is_symlink()
    assert not (env["claude_skills"] / "test-skill").is_symlink()


# ---------------------------------------------------------------------------
# orphan auto-removal (formerly)
# ---------------------------------------------------------------------------

def add_skill_with_formerly(skills_dir: Path, name: str, formerly: str) -> Path:
    """Add a skill that declares a formerly field, replacing an old name."""
    skill_dir = skills_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\n"
        f"name: {name}\n"
        f"description: Renamed skill fixture.\n"
        f"metadata:\n"
        f'  version: "1.0"\n'
        f"  formerly: {formerly}\n"
        f"  disable-model-invocation: true\n"
        f"---\n\n# {name.replace('-', ' ').title()}\n",
        encoding="utf-8",
    )
    return skill_dir


def test_audit_auto_removes_orphan_matching_formerly(env):
    """Orphan symlink whose name matches a 'formerly' field is auto-removed."""
    # Simulate an old skill symlink (orphan — no backing dir)
    old_link = env["claude_skills"] / "old-skill"
    old_link.symlink_to(env["skills_dir"] / "old-skill")

    # New skill declares formerly: old-skill
    add_skill_with_formerly(env["skills_dir"], "new-skill", "old-skill")

    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    assert not old_link.exists(), "Orphan symlink should have been removed"
    assert "Removed orphan symlink" in result.stdout
    assert (env["claude_skills"] / "new-skill").is_symlink()


def test_audit_dry_run_does_not_remove_orphan(env):
    """--dry-run previews orphan removal without deleting anything."""
    old_link = env["claude_skills"] / "old-skill"
    old_link.symlink_to(env["skills_dir"] / "old-skill")

    add_skill_with_formerly(env["skills_dir"], "new-skill", "old-skill")

    result = run_skillmanager(["audit", "--dry-run"], env)
    assert result.returncode == 0
    assert old_link.is_symlink(), "Orphan symlink must survive in dry-run mode"
    assert "dry-run" in result.stdout


def test_audit_flags_unknown_orphan_for_manual_review(env):
    """Orphan with no matching 'formerly' field is flagged, not removed."""
    unknown_link = env["claude_skills"] / "mystery-skill"
    unknown_link.symlink_to(env["skills_dir"] / "mystery-skill")

    add_test_skill(env["skills_dir"], "unrelated-skill")

    result = run_skillmanager(["audit"], env)
    assert result.returncode == 0
    assert unknown_link.is_symlink(), "Unknown orphan must not be auto-removed"
    assert "ORPHAN" in result.stderr


def test_update_removes_formerly_named_skill_dir(env):
    """update --source removes the old skill dir when a new skill declares formerly."""
    import shutil

    # Simulate an old installed skill dir
    old_dir = env["skills_dir"] / "old-skill"
    old_dir.mkdir()
    (old_dir / "SKILL.md").write_text(
        "---\nname: old-skill\ndescription: Old.\nmetadata:\n  version: \"1.0\"\n---\n",
        encoding="utf-8",
    )

    # Source tree has the replacement skill
    source_root = env["skillmanager_dir"].parent / "source"
    source_skills = source_root / "skills"
    source_skills.mkdir(parents=True)
    new_src = source_skills / "new-skill"
    new_src.mkdir()
    (new_src / "SKILL.md").write_text(
        "---\nname: new-skill\ndescription: Renamed.\nmetadata:\n  version: \"1.0\"\n  formerly: old-skill\n---\n",
        encoding="utf-8",
    )

    result = run_skillmanager(["update", "--source", str(source_root)], env)
    assert result.returncode == 0
    assert not old_dir.exists(), "Old skill dir should be removed by update"
    assert (env["skills_dir"] / "new-skill").is_dir()
    assert "Renamed: 1" in result.stdout

    # formerly tag must be stripped from the installed SKILL.md after rename
    installed_text = (env["skills_dir"] / "new-skill" / "SKILL.md").read_text(encoding="utf-8")
    assert "formerly" not in installed_text, "formerly tag should be removed after successful rename"
    assert "Removed 'formerly' tag" in result.stdout
