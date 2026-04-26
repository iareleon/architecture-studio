# Vault :sl calendar {period}

Generate or update a content calendar for a given period (e.g. `2026-05`) in the `social-media` Obsidian vault. Read the vault’s `CLAUDE.md` first.

1. Read all approved posts in `approved/` not yet assigned to a calendar slot
2. Read existing calendar file if present: `wiki/calendar/{period}.md`
3. Assign or suggest post slots across the period by platform and cadence
4. Output: `wiki/calendar/{period}.md` (create or update)
5. Append to `_os/log.md`: `## [date] calendar | {period}`
6. Report: `Calendar updated → wiki/calendar/{period}.md`

Afterward: `references/vault-changelog-protocol.md`.

<!-- sub-skill: content-calendar — not yet authored in SkillsLoom -->
