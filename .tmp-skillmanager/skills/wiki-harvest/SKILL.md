---
name: wiki-harvest
description: Run a structured brain dump session and update the target wiki or knowledge-base page. Reads current page state, asks focused questions, captures answers, advances page status. Invoke for any project or knowledge-base wiki page — configure install personas for your specific wiki system.
metadata:
  version: "1.1"
  disable-model-invocation: true
---
# Wiki Harvest

**Where this should live (long term):** per-wiki conventions belong in each wiki's **`CLAUDE.md`** (status ladder, which pages are curated, links to question-banks / schema). This skill remains the portable **playbook** for live harvest sessions; mirror or summarise the subflows in the wiki that owns the page so headless tools do not need to load Skillforge.

**Main brain:** this file. **Install personas** (optional, install-specific): `persona/meridian.md` (example: arch-agency wiki) · `persona/knowledge-os.md` (example: meta knowledge vault). Configure or replace these for your wiki system. Page schema: `references/wiki-page-schema.md`; questions: `references/question-banks.md`.

Turns brain-dump sessions into structured wiki updates. Read the current page in full first. **Never invent** content — only capture what the user provides.

## Subflows

| File | When |
|------|------|
| `workflows/wiki-harvest-session.md` | Live session |
| `workflows/wiki-harvest-sprint.md` | Approved page → sprint card |

## Status transitions (generic)

```
🟡 harvesting  →  🟠 drafting  →  🟢 approved  →  🚀 in sprint
```

Never skip a stage. Never mark **approved** without explicit user confirmation. Authorisation for who approves each hop is install-specific (see your wiki's `CLAUDE.md` or `persona/` if applicable).

## Guidelines

- Read target wiki page in full; read `decisions/ADR-index.md` in that wiki if it exists.
- **One** focused question at a time — not a list in one message.
- Capture verbatim first, then structure. Flag ADR conflicts — do not resolve silently. Update `last_updated` frontmatter on every write.

## References

- `persona/meridian.md` — example: paths and ADR list for an arch-agency wiki (install-specific)
- `persona/knowledge-os.md` — example: meta knowledge vault, super-wiki vs curated pages (install-specific)
- `references/wiki-page-schema.md` — status values
- `references/question-banks.md` — topic questions
