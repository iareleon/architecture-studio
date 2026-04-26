---
title: Getting Started
---

# Getting Started

## Prerequisites

- Bash 4.0 or later (`bash --version`) — macOS ships Bash 3, install via `brew install bash`
- Standard Unix tools: `find`, `ln`, `mv`, `cp`, `grep`, `sed`
- Git (for cloning)
- `~/.local/bin` writable (or a custom `$PATH` location)

## Install

### 1. Clone the repository

```bash
git clone https://github.com/Choreogrifi/skill-manager.git
cd skill-manager
```

### 2. Run the installer

```bash
bash scripts/install.sh
```

The installer will prompt you for:
- **Install directory** — where SkillsLoom assets live (default: `~/.skillsloom`)
- **LLM targets** — which LLMs you use: `claude`, `gemini`, or both
- **Email** — optional, for skill proposal notifications
- **System skills mode** — `Always-on` (skill detection and memory management embedded in `model.md`, active every session) or `Manual` (invoke `/skill-manager` or `/brain-manager` when needed). Default: `Manual`

It then:
- Detects available tools (`git`, `gh`, `gcloud`, `terraform`) and warns if any are missing
- Writes your configuration to `~/.skillsloom/config.yaml`
- Copies the starter skills (never overwrites existing ones)
- Creates symlinks for all `active` skills in your LLM target directories
- Installs the `skillmanager` CLI to `~/.local/bin/skillmanager`
- Adds `~/.local/bin` to your PATH (if not already present)

### 3. Reload your shell

```bash
source ~/.zshrc   # or ~/.bashrc
```

### 4. Verify the installation

```bash
skillmanager doctor
skillmanager ls
```

## Testing New Skills

Use the test environment scripts to validate skills under development without touching your production install.

```bash
# Set up an isolated test environment
bash scripts/test-env-setup.sh

# Tear it down when done
bash scripts/test-env-teardown.sh
```

**What `test-env-setup.sh` does:**
- Creates `.tmp-skillmanager/` in the repo root (`TMP_SKILLMANAGER_DIR`) with a full skills directory structure.
- Copies every `skills/<name>/` directory that contains a `SKILL.md` from the repo into the test environment.
- Creates symlinks at `~/.claude/skills/<name>` (or `~/.gemini/skills/<name>`) **only** for skills that have no existing production symlink. This makes test skills visible to your LLM immediately.
- Records every created symlink in `.tmp-skillmanager/.test-manifest`.

**What `test-env-teardown.sh` does:**
- Removes only the symlinks listed in `.test-manifest` — production symlinks are never touched.
- Removes the `.tmp-skillmanager/` directory entirely.

**Boundary rule — `SKILLSLOOM_DIR` vs `TMP_SKILLMANAGER_DIR`:**

| Variable | Purpose | Managed by |
|---|---|---|
| `SKILLSLOOM_DIR` | Production install (`~/.skillsloom` by default) | `install.sh` and `uninstall` only |
| `TMP_SKILLMANAGER_DIR` | Test environment (`.tmp-skillmanager/` in repo) | `test-env-setup.sh` and `test-env-teardown.sh` |

Never set `SKILLSLOOM_DIR` manually for testing — doing so risks corrupting your production configuration.

## First Commands

```bash
# See each skill’s metadata.status and symlink health
skillmanager ls

# Edit metadata.status in skills/<name>/SKILL.md, then:
skillmanager audit

# Check for invariant violations
skillmanager status

# Learn about memory files and token costs
skillmanager memory-help
```

## Uninstall

```bash
skillmanager uninstall
```

Walks you through removing symlinks, the binary, and optionally the skill data directory and PATH entries. Skill data is never deleted without a separate explicit confirmation — a reinstall after uninstall will find your skills intact.
