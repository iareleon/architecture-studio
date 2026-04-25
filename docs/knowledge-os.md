---
title: Knowledge OS and Obsidian meta
---

# Knowledge OS + Skillforge

This page defines how **Skillforge** (skills, memory, `skillmanager audit`) fits with an **Obsidian “Knowledge OS”** whose **master vault** is `meta` — a registry and automation hub for many vaults.

## Roles

| Piece | Role |
|-------|------|
| **Meta vault** (`…/Obsidian/meta`) | Inbox for capture, `_os/` registry, `wiki/` domain pages, scripts; drives `super-wiki-sync` / `folder-structure-sync` for global indices. |
| **Domain vaults** | Each has `CLAUDE.md` and `_os/index.md` (and optionally `raw/`, `wiki/`, etc.). |
| **Skillforge** | Canonical install under `SKILLMANAGER_DIR` (default `~/.skillmanager`); `skillmanager audit` places symlinks in `~/.claude/skills` (and configured dirs). |

Skillforge does **not** run Obsidian or watch the filesystem. It governs **which skills the agent can load**. The meta pipeline governs **where notes go** and **how indices refresh**.

## Environment variables

| Variable | Default | Purpose |
|----------|---------|----------|
| `SKILLMANAGER_DIR` | `~/.skillmanager` (or `install_dir` in `config.yaml`) | Root containing `skills/`. All Skillforge skills live here. |
| `OBSIDIAN_ROOT` | `~/Obsidian` | Base directory for all Obsidian vaults. |
| `OBSIDIAN_META` | `$OBSIDIAN_ROOT/meta` | Master Knowledge OS vault path. |
| `CHOREOKIT_DIR` | (unset) | Optional. If you keep **Knowledge OS op-skills** (e.g. `core/super-wiki-sync`) in a separate tree (such as `~/choreokit`), set this so docs and `skillmanager knowledge-os` can mention both layouts. |

Copy [knowledge-os/knowledge-os.env.example](../knowledge-os/knowledge-os.env.example) and adjust.

## Symlink authority (one truth on disk)

Agents read skills from **`~/.claude/skills/<name>`** (symlinks) or other paths in `~/.skillmanager/config.yaml`.

**Rule:** There must be a **single source directory** for each skill name that your workflow uses.

1. **Recommended:** Install Skillforge; keep all first-party skills only under `$SKILLMANAGER_DIR/skills/<name>/`. Run `skillmanager audit` so `~/.claude/skills/<name>` → `$SKILLMANAGER_DIR/skills/<name>`.

2. **Knowledge OS op-skills** (inbox-classifier, super-wiki-sync, process-inbox) may live in a **separate** repo (e.g. choreokit) **or** be symlinked *into* `SKILLMANAGER_DIR/skills/` as optional extra entries — but **do not** duplicate the same skill name in two real directories; pick one target for `~/.claude/skills/<name>`.

3. If Cowork or docs reference `~/choreokit/core/super-wiki-sync.md`, that path is **install-specific**. Align your machine by either symlinking choreokit into the expected layout or editing scheduled task instructions to the path where those files actually live after `skillmanager audit`.

## Generated files (do not hand-edit)

The meta vault and Knowledge OS skills rely on **machine-generated** indices. Do not hand-edit and expect changes to stick:

- `meta/CLAUDE.md` — the section declaring the generated-file policy is managed; do not remove it, but you may add your own content above or below
- `meta/_os/index.md` (where maintained by `super-wiki-sync`)
- `meta/_os/_structure.md` (from `folder-structure-sync`)
- `meta/wiki/{vault}.md` per-vault pages from `super-wiki-sync`
- `~/Obsidian/_super-wiki.md` (global index)

After file operations in a vault, the prescribed chain is: **`folder-structure-sync` → `super-wiki-sync`** (per your op-skill definitions).

**Contrast:** `meta/wiki/*.md` **domain pages** (e.g. `business`, `product`) that you curate for *description/scope* are not the same as the **per-vault registry rows** `meta/wiki/{vault}.md` produced by `super-wiki-sync`. The [wiki-harvest](../skills/wiki-harvest/SKILL.md) skill’s `persona/knowledge-os.md` explains which is which.

## Agent hooks (layers)

| Layer | Use |
|-------|-----|
| **Claude Code / Cursor** | PostToolUse: validate YAML/Markdown after edits. |
| **Git / `skillmanager git commit`** | Skill naming and repo checks. |
| **Claude Cowork** | Scheduled inbox processing and super-wiki refresh (no daemon required). |
| **OS scripts** (optional) | e.g. inbox FSEvents + headless `claude` — install-specific. |

## CLI checks

```bash
skillmanager knowledge-os
```

Verifies `OBSIDIAN_META`, expected layout, and Skillforge symlinks for **wiki-harvest** and **vault-paths** (implemented in the `skillmanager` CLI). Knowledge OS inbox routing uses separate `classify` / `process-inbox` skills in your `~/.claude/skills` layout when present.

## See also

- [How It Works](how-it-works.md) — Skillforge filesystem model
- [Cowork task templates](../knowledge-os/cowork/) — versioned prompts for Claude Cowork
- [Vault paths](../skills/vault-paths/references/vault-map.md) — canonical paths including meta
