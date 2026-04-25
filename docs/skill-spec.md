---
title: SKILL.md Specification
---

# SKILL.md Specification

See also **[Domain (skill) layout](domain-layout.md)** — research-backed standard for folder shape, naming, and dependencies.

## Directory naming

Every skill is a directory under `$SKILLMANAGER_DIR/skills/`. The **folder name** is the skill id (kebab-case). There is no `-sme` or `-wf` suffix — merge former SME and workflow into one tree when they described the same domain.

**Name rules**

- Lowercase letters, digits, and hyphens; must start with a letter
- Not a reserved top-level name: `review`, `deactivated`, `staging`, `decommissioned`, `sme`, `workflow` (do not use as a skill folder name)
- Optional `-sys` suffix for rare system/validator skills

**Visibility / lifecycle** is `metadata.status` in `SKILL.md` (all skills live at `skills/<name>/`):

| `metadata.status` | LLM symlinks |
|-------------------|----------------|
| `active` (default if omitted) | Yes — `~/.claude/skills/<name>` (and configured Gemini path) |
| `staging` | Staging dirs only: `~/.claude/skills-staging/<name>`, etc. |
| `review`, `deactivated`, `decommissioned` | No symlinks |

After changing status, run `skillmanager audit` to align symlinks on disk.

## SKILL.md format

```markdown
---
name: <skill-name>
description: <one line — when to invoke>
metadata:
  version: "1.0"
  status: active
  related-skills: [<other-skill>, ...]
  disable-model-invocation: true
---

# Title

Router table or short invariants; long procedures → `workflows/`, facts → `references/`.
```

### Required frontmatter

| Field | Rules |
|-------|--------|
| `name` | Must equal the directory name |
| `description` | One non-empty line |
| `metadata.version` | e.g. `"1.0"` |
| `metadata.disable-model-invocation` | `true` |

### Optional

| Field | Purpose |
|-------|---------|
| `metadata.status` | `active` (default), `staging`, `review`, `deactivated`, or `decommissioned` — controls LLM symlinks; run `skillmanager audit` after edits |
| `metadata.memory-file` | **Rare.** Path to a supplemental file under the skill (legacy `memory/baseline.md`). Most skills omit this; use `SKILL.md` + optional `persona/`. |
| `metadata.related-skills` | Other skill names this one coordinates with |

**Router pattern:** keep `SKILL.md` under ~100 lines; put menus and long flows in `workflows/*.md`.

## Directory layout (example)

```
skills/
  git/
    SKILL.md
    persona/
    workflows/
    references/
```

## Workflows (procedures)

Files in `workflows/` are loaded on demand. **Filenames** are kebab-case and describe the workflow; do **not** add role suffixes like `-sf` (the `workflows/` directory already classifies the file). They may have YAML frontmatter for documentation; CI only validates top-level `SKILL.md` per skill.

## Validation

`skillmanager audit` and `.github/workflows/validate.yml` enforce naming and frontmatter.
