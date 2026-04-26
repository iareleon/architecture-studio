# Scripts

CLI and maintenance scripts for SkillsLoom. All scripts are written in Python 3 and run on macOS, Linux, and Windows without any additional dependencies beyond the Python standard library.

---

## Scripts reference

### `skillmanager.py`

The main CLI. Installed as `skillmanager` in `~/.local/bin/` (Unix/macOS) or `%LOCALAPPDATA%\Programs\skillmanager\` (Windows) during setup.

```bash
skillmanager help         # full command reference
skillmanager ls           # list skills: metadata.status vs symlinks
skillmanager audit        # align LLM symlinks with metadata.status in each SKILL.md (alias: sync)
skillmanager status       # check status ↔ symlinks
skillmanager lint [file]  # check markdown quality
skillmanager doctor       # check environment, tools, and PATH
skillmanager config       # show current configuration
skillmanager memory-help  # guide to memory files and token costs
skillmanager version      # print installed version
```

Or invoke directly without installation:

```bash
python3 scripts/skillmanager.py ls
```

---

### `install.py`

Interactive installer. Run once to set up SkillsLoom for the first time, or again to update an existing install.

```bash
python3 scripts/install.py
```

What it does (summary):
1. Asks where to install (default: `~/.skillsloom`) and which LLMs to use
2. Detects available tools (git, gh, glab, gcloud, terraform)
3. Creates `~/.skillsloom/config.yaml` with your choices
4. Copies starter skills into `$SKILLSLOOM_DIR/skills/`
5. Sets up optional `model.md` persona
6. Installs `skillmanager` to `~/.local/bin/` (Unix) or `%LOCALAPPDATA%\Programs\skillmanager\` (Windows)
7. Runs `skillmanager audit` (symlinks from each skill's `metadata.status`)
8. Adds `~/.local/bin/` to your shell's PATH (Unix), optional git hooks, install checksums

Safe to re-run — it is idempotent.

**Platform notes:**
- **Windows**: Symlinks require Developer Mode or administrator rights. Enable via _Settings → System → For Developers → Developer Mode_.
- **macOS/Linux**: No special requirements.

---

### `check_skill_names.py`

Validates that all skill directory names follow the naming convention.

```bash
python3 scripts/check_skill_names.py          # check all skills
python3 scripts/check_skill_names.py --staged # check only staged files (for pre-commit)
```

This script is used in CI (`.github/workflows/validate.yml`) and in the pre-commit hook.

Exit code 0 = all names comply. Exit code 1 = violations found.

---

### `test_env_setup.py`

Scaffolds an isolated test environment without touching production skills or LLM context files.

```bash
python3 scripts/test_env_setup.py
```

---

### `test_env_teardown.py`

Removes the test environment created by `test_env_setup.py`.

```bash
python3 scripts/test_env_teardown.py
```

---

### `agents.py`

**DEPRECATED** — wrapper that calls `skillmanager.py`. Update any scripts using `agents` to call `skillmanager` instead.

---

### `hooks/`

Git hooks for this repository. Used during development of SkillsLoom itself.

To install the hooks:
```bash
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit   # Unix/macOS only
```

The pre-commit hook runs `check_skill_names.py --staged` before each commit to prevent naming violations from being committed. The hook is a Python script and works on all platforms where Python 3 is available.
