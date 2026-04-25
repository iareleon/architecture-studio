# Wiki harvest — Meridian install context

Load when the target wiki lives in the **arch-agency (Meridian)** vault. General process is in `../SKILL.md`.

## System paths (this install)

- Meridian vault: `/Users/leond/Obsidian/arch-agency`
- Thought Scaffold: `/Users/leond/Obsidian/the-thought-scaffold`
- Read `decisions/ADR-index.md` before any session—never re-derive confirmed decisions.
- Read `context/key-decisions.md` for non-negotiables when present.

## Status transitions (authorisation)

| From | To | Who authorises |
|------|-----|----------------|
| 🟡 harvesting | 🟠 drafting | Agent after gaps filled |
| 🟠 drafting | 🟢 approved | User only—never agent |
| 🟢 approved | 🚀 in sprint | Agent after sprint card created |

## Session discipline

- One question at a time (max 8 per session; stop when gaps filled). Use `references/question-banks.md`.

## Confirmed ADRs (non-negotiable in this program)

- ADR-001: Hexagonal architecture
- ADR-002: MCP protocol for integrations
- ADR-003: LiteLLM for LLM calls
- ADR-004: Kuzu default graph store
- ADR-005: Local Docker Compose first
- ADR-006: Python + TypeScript/React
- ADR-007: Markdown only
- ADR-009: No ADK in product layer
- ADR-016: Product name is Meridian

Update this file when ADRs or paths change.
