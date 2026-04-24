# 2026-04-22-13-48-add-audit-selection-rule

**Status: [done]**

## Summary

- Updated `SKILL.md` for the `auditor` skill.
- Added a new `Selection` step to the Workflow section, requiring the system to always ask the user which audit must be done and by which persona before proceeding.

## Justification

Ensures user intent is explicitly captured and the correct audit persona is selected before the system executes an automated audit, avoiding assumptions.

## Impact

- **Systems:** Auditor Skill Workflow
- **Documents:** `C:\Users\leond\.gemini\skills\auditor\SKILL.md`