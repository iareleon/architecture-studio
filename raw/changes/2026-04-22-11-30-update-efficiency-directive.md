# 2026-04-22-11-30-update-efficiency-directive

**Status: [done]**

## Summary
- Updated `GEMINI.md` with a new **Cost Efficiency** directive to exclude `/llm/changes` and `/llm/discovery` from implicit reads.
- Clarified the removal of redundant `format_meeting_notes.py` placeholder.
- Updated project documentation to reflect the absence of meetings, resolving the audit gap.

## Justification
User directive to optimize token usage by preventing the LLM from crawling high-volume audit and discovery logs unless explicitly requested. Structural cleanup ensures only active, functional scripts are maintained.

## Impact
- **Systems:** Workspace Governance, LLM Context Management.
- **Documents:** `GEMINI.md`, `llm/folder-structure.md`, `raw/reports/2026-04-22-11-20-structural-audit.md`.
