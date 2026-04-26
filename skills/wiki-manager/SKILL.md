---
name: wiki-manager
description: "Knowledge OS — config, inbox pipeline, dispatch between meta and vaults, wiki and structure sync, harvest sessions, and sprint cards from wiki. Use for anything like process my inbox, move this note to a vault, refresh the super-wiki, run a harvest, or set up `wiki-manager.config` — when in doubt, route knowledge-base work here even if the user says \"put this in the wiki\" without naming the tool."
metadata:
  version: "1.0"
  disable-model-invocation: true
  formerly: wiki-harvest
---

# Wiki Manager

Central skill for all Knowledge OS operations: inbox processing, vault sync, wiki harvest sessions, and sprint cards.

**Config:** read `{OBSIDIAN_META}/wiki-manager.config.yaml` at the start of every operation. Run `wiki-manager-config` once after install to create it. If `OBSIDIAN_META` is not set, check terminal environment variables or ask the user.

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
      ↓  inbox-classify (manual CLI run)
[meta/inbox/review]
      ↓  user: review → move to approved
[meta/inbox/approved]
      ↓  inbox-dispatch (manual CLI run)
[{vault}/inbox/raw]
      ↓  user: review → move to approved
[{vault}/inbox/approved]
      ↓  vault-inbox-sync (manual CLI run)
[{vault}/raw/] + wiki updated
```

## Rules (why, not just what)

1. Read `{OBSIDIAN_META}/wiki-manager.config.yaml` before every operation — the pipeline paths and vault list live there; without it, writes land in the wrong place and are hard to undo.
2. `ambiguous` inbox items: stop and show them to the user. Guessing a destination bakes a wrong link into the vault graph; a human can disambiguate once; manual triage avoids hard-to-reverse routing errors.
3. Green (🟢) approval: only a human. Status is a trust signal; automating "approved" would merge unreviewed content into the canonical wiki.
4. Do not hand-edit generated views (`_super-wiki.md`, `meta/wiki/{vault}.md`, `_structure.md`) — the sync jobs own them. Edits are overwritten and create merge confusion between "truth in notes" and "stale in generated index".
5. Stay inside the op's target scope. Broad writes risk rewriting neighbouring folders during manual runs.
6. Treat `{vault}/raw/` as append-only: it is the immutable capture layer. Only `vault-inbox-sync` adds there so derived wiki pages always trace to an auditable source file.

## References

- `references/config-schema.md` — `wiki-manager.config.yaml` format and all fields
- `references/wiki-page-schema.md` — page frontmatter and status ladder
- `references/question-banks.md` — focused questions by wiki topic
- `persona/knowledge-os.md` — meta vault install context (load for inbox and super-wiki ops)
