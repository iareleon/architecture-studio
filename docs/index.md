---
title: skill-manager
---

# skill-manager

**Version 2.0.0**

A filesystem-based skill management system for LLMs.

Skills are directories under `skills/<name>/`. `metadata.status` in each `SKILL.md` (with `skillmanager audit`) controls symlinks and LLM visibility — no database, no background services.

## Install

**Homebrew (macOS / Linux)**

```bash
brew tap choreogrifi/skill-manager
brew install skill-manager
```

**curl one-liner**

```bash
curl -fsSL https://raw.githubusercontent.com/Choreogrifi/skill-manager/main/scripts/install.sh | bash
```

**From source**

```bash
git clone https://github.com/Choreogrifi/skill-manager.git
cd skill-manager
bash scripts/install.sh
```

## Quick Start

```bash
# List skills: metadata.status vs symlinks
skillmanager ls

# After editing metadata.status in skills/<name>/SKILL.md:
skillmanager audit

# Check symlink health
skillmanager status

# Self-check the environment
skillmanager doctor
```

## Learn More

- [Getting Started](getting-started.md) — prerequisites and first steps
- [How It Works](how-it-works.md) — the filesystem model, skill types, memory system, and self-discovery
- [Skill Catalog](skill-catalog.md) — all built-in SME and workflow skills
- [CLI Reference](cli.md) — all commands with examples
- [SKILL.md Specification](skill-spec.md) — skill format and naming rules
- [Domain (skill) layout](domain-layout.md) — self-contained tree, SRP, and dependencies without duplication
- [Knowledge OS + Obsidian meta](knowledge-os.md) — multi-vault registry, env vars, hooks, and Cowork templates
