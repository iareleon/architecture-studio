# Vault :sl goal {goal}

Track or update a personal goal in the `personal` Obsidian vault. Read the vault’s `CLAUDE.md` first.

1. Check `wiki/goals/` for an existing goal page matching the slug
2. If new: create `research/active/{goal-slug}.md` with goal definition, success criteria, milestones, and current status
3. If update: read existing wiki page and draft an update to milestones/status
4. Set `requires_confirmation: true` before any write
5. On approval: write or update `wiki/goals/{goal-slug}.md`
6. Append to `_os/log.md`: `## [date] goal | {goal-slug}`

Afterward: `references/vault-changelog-protocol.md` for the full log format.

<!-- sub-skill: goal-tracker — not yet fully merged -->
