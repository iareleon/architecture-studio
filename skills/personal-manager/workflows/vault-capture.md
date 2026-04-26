# Vault :sl capture {reflection}

Process a soul reflection or personal raw capture in the `personal` Obsidian vault. Read the vault’s `CLAUDE.md` first.

1. Read the raw file — do not modify it
2. Identify themes: fears, desires, wins, commitments, questions
3. Set `requires_confirmation: true` — the user must explicitly approve; raw emotion mis-filed is worse than a delay
4. Present summary to user and ask for approval before writing
5. On approval: output `research/active/{YYYYMMDD}-{theme-slug}.md`
6. Append to `_os/log.md`: `## [date] ingest | {theme-slug}`
7. Report: `Capture drafted → research/active/{theme-slug}.md. Awaiting your review.`

Afterward: `references/vault-changelog-protocol.md` for the full log format.

<!-- sub-skill: soul-capture — could merge with personal-soul-write over time -->
