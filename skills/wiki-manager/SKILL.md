---
name: wiki-manager
description: Knowledge OS — inbox classification, vault dispatch, wiki sync, harvest sessions, and sprint cards. All wiki and knowledge-base operations route through this skill.
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# Wiki Manager

Central skill for all Knowledge OS operations: inbox processing, vault sync, wiki harvest sessions, and sprint cards.

**Config:** read `{OBSIDIAN_META}/wiki-manager.config.yaml` at the start of every operation. Run `wiki-manager-config` once after install to create it. If `OBSIDIAN_META` is not set, check the Cowork task or ask the user.

## Workflows

| Workflow | Purpose |
|----------|---------|
| `workflows/wiki-manager-config.md` | First install or config change — creates/updates `wiki-manager.config.yaml` in `OBSIDIAN_META` |
| `workflows/inbox-classify.md` | Step 1 — classify `meta/inbox/raw/` → `meta/inbox/review/` |
| `workflows/inbox-dispatch.md` | Step 2 — dispatch `meta/inbox/approved/` → `{vault}/inbox/raw/` |
| `workflows/vault-inbox-sync.md` | Step 5 — process `{vault}/inbox/approved/` → final location + wiki update |
| `workflows/wiki-sync.md` | On-demand — refresh `_super-wiki.md` and per-vault pages for changed vaults |
| `workflows/folder-structure-sync.md` | After any folder change — update `_structure.md` for one folder |
| `workflows/wiki-harvest-session.md` | Live brain dump for a target wiki page |
| `workflows/wiki-harvest-sprint.md` | Convert an approved (🟢) wiki page into a sprint card |

## Inbox pipeline

```
[meta/inbox/raw]
      ↓  inbox-classify (automation)
[meta/inbox/review]
      ↓  user: review → move to approved
[meta/inbox/approved]
      ↓  inbox-dispatch (automation)
[{vault}/inbox/raw]
      ↓  user: review → move to approved
[{vault}/inbox/approved]
      ↓  vault-inbox-sync (automation)
[{vault}/raw/] + wiki updated
```

## Rules

1. Read `{OBSIDIAN_META}/wiki-manager.config.yaml` before every operation.
2. Never auto-route `ambiguous` classified files — always flag for user review.
3. Never advance a wiki page to 🟢 approved — user only.
4. Never hand-edit auto-generated files: `_super-wiki.md`, `meta/wiki/{vault}.md`, `_structure.md`.
5. Never write outside the current operation's target scope.
6. `{vault}/raw/` is immutable and append-only — never modify or delete files there once placed. It is the source layer from which wiki content is derived. Only `vault-inbox-sync` may write to `raw/`.

## References

- `references/config-schema.md` — `wiki-manager.config.yaml` format and all fields
- `references/wiki-page-schema.md` — page frontmatter and status ladder
- `references/question-banks.md` — focused questions by wiki topic
- `persona/knowledge-os.md` — meta vault install context (load for inbox and super-wiki ops)
