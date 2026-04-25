# Authoring templates

Copy these from the `skill-manager` skill (this directory) to scaffold new skills, workflows, and reference files. See [Domain layout](../../../docs/domain-layout.md) for the full standard.

---

## Table

| Template | Use |
|----------|-----|
| `expertise-skill-template.md` | New SME-style `SKILL.md` |
| `workflow-skill-template.md` | New workflow `SKILL.md` |
| `workflow-file-template.md` | Body for a new `workflows/*.md` file |
| `workflow-fragment.md` | Optional legacy-style `SKILL.md` body; prefer a thin `SKILL.md` plus `workflows/` |
| `reference-doc.template.md` | A lazy-loaded `references/*.md` file |
| `persona/model.md` | Local persona file in `$SKILLMANAGER_DIR` (not committed; see install script) |
| `persona/system-skills-always-on.md` | System capabilities block (always-on install mode) |
| `persona/system-skills-manual.md` | System capabilities block (manual install mode) |

**Durable context:** author the main rules in `SKILL.md`; add `persona/<topic>.md` for distinct sub-topics; use project `CLAUDE.md` for workspace facts. Legacy per-skill `memory/baseline.md` is discouraged. Scaffolds for optional memory-style files: `skills/memory/references/scaffold-*.md`.

---

## How to use

1. `cp` the template to the right path under `skills/`.
2. Replace `<PLACEHOLDER>` values; remove guide comments when done.
3. Run `skillmanager audit` (or your project’s skill validation).

**Name field:** `name:` must match the directory name (e.g. `name: my-api` for `skills/my-api/`).
