---
title: How It Works
---

# How It Works

## Skills on disk, visibility in frontmatter

Every skill is **one** directory: `skills/<name>/` (kebab-case id). There are no per-state subfolders. Whether an LLM can load a skill is controlled by `metadata.status` in that skill’s `SKILL.md` and by symlinks that `skillmanager audit` creates or removes.

Omitting `metadata.status` is treated as `active` (visible when symlinks are present).

| `metadata.status` | Effect |
|---|---|
| `active` | Symlinks in `~/.claude/skills/<name>`, `~/.gemini/skills/<name>`, or paths from `config.yaml` |
| `staging` | Symlinks in `~/.claude/skills-staging/`, etc., only (test without polluting default skill dirs) |
| `review` / `deactivated` / `decommissioned` | No LLM symlinks; skill files remain under `skills/<name>/` |

Change status in `SKILL.md`, then run `skillmanager audit` so the symlinks on disk match.

## Symlinks as the visibility gate

LLM agents (Claude, Gemini) discover skills by scanning their designated directories:

```
~/.claude/skills/
~/.gemini/skills/
```

When a skill is **active** (default), a symlink is created in each of these directories pointing to the skill directory:

```
~/.claude/skills/architect  →  $SKILLMANAGER_DIR/skills/architect/
~/.gemini/skills/architect  →  $SKILLMANAGER_DIR/skills/architect/
```

When a skill is not active in metadata (or is `review` / `deactivated` / `decommissioned`), those production symlinks should not exist after `skillmanager audit`. The agent then cannot see the skill.

Visibility is controlled entirely at the filesystem level — no agent config, no allowlists, no restart required.

## The Invariant

There is one rule that must always hold:

> Every **active** skill under `skills/<name>/` has a symlink in `~/.claude/skills/<name>` (same for configured Gemini path).

The `skillmanager audit` command detects and repairs violations automatically.

## The `SKILLMANAGER_DIR` Variable

All paths are derived from `SKILLMANAGER_DIR` (default: `~/.skillmanager`, configured at install time):

```bash
SKILLMANAGER_DIR="${SKILLMANAGER_DIR:-$HOME/.skillmanager}"
SKILLS_DIR="${SKILLMANAGER_DIR}/skills"
```

Override it to run against a test environment without touching live data:

```bash
SKILLMANAGER_DIR=/tmp/sf-test skillmanager ls
```

## CLI vs LLM — Division of Responsibility

The `skillmanager` CLI and the LLM skills cover distinct concerns:

| Capability | CLI (`skillmanager`) | LLM (skills) |
|---|---|---|
| Skill lifecycle (activate, deactivate, review, rm) | ✓ | — |
| Skill creation and authoring | — | ✓ via `skill-manager` |
| Git operations (commit, push, branch, clone…) | ✓ via `skillmanager git` | ✓ via `git` |
| GitHub PRs / GitLab MRs | ✓ via `skillmanager git pr/mr` | ✓ via `git` skill workflows |
| Skill naming gate on commit | ✓ built into `skillmanager git commit` | — |

Git is available in both because the CLI is used outside of an LLM session (e.g. in CI, pre-commit hooks, or terminal workflows). The LLM path adds interactive guidance and dry-run summaries; the CLI path is for scripted or fast terminal use.

## Why No Database?

- **Observability**: `skillmanager ls` or `ls $SKILLMANAGER_DIR/skills/` shows the complete system state instantly.
- **Durability**: No corruption risk — there's nothing to corrupt beyond a directory rename.
- **Portability**: The entire skill set is a directory tree. Copy it, version it, back it up with standard tools.
- **Debuggability**: `find`, `ls -la`, and `readlink` are sufficient to diagnose any issue.

## Skill content types

Each **directory** is one activatable skill. `SKILL.md` is the entrypoint; long procedures live in `workflows/`, facts and tables in `references/`. Content may mix routing and expertise — structure follows the domain, not a separate type label.

## Cross-skill use

Routers load other files by path. Examples: the `git` skill follows `workflows/github-platform.md` or `workflows/gitlab-platform.md`; `devops` can call the `cloud-engineer` skill’s inventory workflows when you need a live project baseline.

## Cross-Skill Delegation

The `related-skills` metadata field can declare coordination:

```
git        →  (internal) GitHub vs GitLab workflows
devops     →  cloud-engineer (inventory), devops Terraform references
documenter →  diagrammer (Mermaid), documenter workflows
```

## Durable context (skills vs project)

Each skill’s **`SKILL.md`** is the main brain. Distinct sub-topics (e.g. Python vs React) live in optional **`persona/<topic>.md`**. **Project** facts and preferences belong in the workspace **`CLAUDE.md`** (or equivalent), not a duplicate per-skill `memory/baseline.md` unless you deliberately keep a legacy file.

The **`memory`** skill helps record approved edits to those targets. Small context files (persona, legacy memory) are typically capped at ~40 lines; split if they grow.

## Session Memory and `/clear`

Only `model.md` (your persona file, symlinked to `CLAUDE.md`) persists after `/clear`. All invoked skill context is removed. Skills remain available as slash commands and can be re-invoked in the new session.

**System skills** (skill detection, memory management) operate in one of two modes set at install:

| Mode | Behaviour |
|---|---|
| Always-on | Rules embedded in `model.md` — active every session, survive `/clear` |
| Manual | Invoked as `/skill-manager` or `/memory` when needed — cleared by `/clear` |

Switch modes at any time: invoke `/memory` → "toggle system skills".

## Workflows (procedural files)

Workflow skills can delegate to **workflows** — narrow processes that handle one specific operation. They are loaded lazily: only the matching file is read when needed.

```
git
  └── workflows/
        git-clone.md         ← loaded when the user wants to clone
        git-branch.md        ← branch operations
        git-conflict.md      ← merge conflicts
```

These files are plain Markdown; optional YAML is allowed for documentation. They are not separate symlink targets — only the skill directory is installed.

## Self-Discovery

Skills that have an improve-style workflow (e.g. `workflows/mermaid-improve.md` under `diagram`) often follow the same standard pattern:

1. **Discover** — audit the relevant content using the skill's read/audit workflow
2. **Plan** — present findings as a structured improvement plan (plan mode only)
3. **User approves** — no changes without explicit confirmation
4. **Apply** — each change shown as before/after diff
5. **PR** — a pull request is created via `git` skill / `skillmanager git` for repository owner review
