# 2026-04-22-12-15-enable-git-manager-cli

**Status: [done]**

## Summary

- Create `skills/git-manager/scripts/` directory.
- Implement `prepare_commit.cjs` to automate Git diff capture and change scaffolding.
- Update `skills/git-manager/SKILL.md` with "Automation & Guardrails" section.
- Update `README.md` to reflect `git-manager` CLI capability.
- Update `llm/folder-structure.md` to include new directories.

## Justification

Enabling `git-manager` as a CLI tool improves the developer workflow by allowing them to trigger Git context capture directly from the terminal. This maintains the "Architecture Studio" pattern where CLI scripts act as guardrails and triggers for AI-driven synthesis.

## Impact

- **Systems:** Git management workflow, Workspace Governance.
- **Documents:** `skills/git-manager/SKILL.md`, `README.md`, `llm/folder-structure.md`, `llm/change-log.md`.
