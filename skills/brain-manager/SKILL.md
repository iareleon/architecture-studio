---
name: brain-manager
description: Detects memory-change intent in user input and updates the correct workspace memory file with explicit user approval. Invoke directly or trigger automatically from natural language patterns.
metadata:
  version: "1.1"
  disable-model-invocation: true
---
# Brain Manager

**Main brain:** this file. Skills no longer use per-skill `memory/baseline.md` as a default; route durable facts to **project** or **persona** files (see table below) instead of a duplicate “layer” under every skill.

Detects when the user wants to record, update, or remove a fact. Identifies the target file, shows a before/after diff, writes **only** on explicit approval.

## Trigger patterns

- "remember that…", "note that…", "going forward…"
- "update my memory / profile / preferences…"
- "forget…", "remove from memory…", "I no longer…"
- "I prefer…", "from now on…", "always…", "never…"
- "Add global rule…", "Add local rule…"

## Classify the memory → target (priority)

| User intent | Preferred target |
|-------------|------------------|
| **Project / product** context (this repo) | Project root `CLAUDE.md`, `AGENTS.md`, or a doc path the user names |
| **User-global** (all workspaces) | User-level rules / `~/.claude/CLAUDE.md` (or equivalent)—**high impact;** confirm scope before editing |
| **Per-skill overlay** (optional, narrow topic) | `skills/<skill-id>/persona/<topic>.md` when that skill already uses `persona/` (e.g. `development-engineer/persona/python.md`) |
| **Legacy** | `skills/<skill>/memory/baseline.md` only if the file still exists and the user explicitly wants to keep using it—**do not** create new per-skill `memory/baseline.md` for skills that have migrated to main `SKILL.md` |

If the target is ambiguous, ask: project vs user-global vs which skill `persona/`.

## Workflow

1. **Read** the full target file before drafting.
2. **Propose** a before/after diff; for removals, archive: `<!-- archived: YYYY-MM-DD: <reason> -->`.
3. **Write** on explicit "yes" only. Confirm: `Memory updated: <path>`.
4. Keep **~40 lines** per small memory file; split into another scoped file if needed (suggest a path).

## Scaffolding (stubs, list, archive, toggles)

- Create stub: `workflows/brain-create.md`
- List / view / archive: `workflows/brain-audit.md`
- System skills mode: `workflows/brain-system-toggle.md`

## Other

- **Directive hygiene:** root instruction edits are high-risk—summarise impact and get approval.
- **Change / discovery logging:** use project trail where the repo keeps it.
- **Librarian templates:** `references/librarian-templates/` (optional). Adapt to `${SKILLFORGE_DIR}`; no proprietary path assumptions.

## References

- `references/librarian-templates/changes.template.md`
- `references/librarian-templates/discovery.template.md`
