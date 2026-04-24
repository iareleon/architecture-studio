# 2026-04-22-12-30-restructure-llm-and-raw

**Status: [done]**

## Summary

- Relocated `changes/`, `discovery/`, `change-log.md`, and `discovery-log.md` from `llm/` to `raw/`.
- Updated `GEMINI.md` to reflect the new Layer definitions (Lean LLM, Traceability in Raw).
- Updated `llm/folder-structure.md` map.
- Updated `README.md` references.
- Updated `skills/git-manager/scripts/prepare_commit.cjs` to use new paths.
- Updated `skills/auditor/assets/templates/folder-structure.template.md`.
- Updated `skills/librarian/assets/templates/change-log.template.md`.
- Updated workflow paths in `skills/librarian/SKILL.md`, `skills/researcher/SKILL.md`, `skills/skill-creator/SKILL.md`, and `skills/brain-manager/SKILL.md`.

## Justification

As per user directive, the `/llm/` directory is now lean, containing only core memory files. Traceability records (logs and individual change/discovery files) have been moved to the `/raw/` source layer to better distinguish between system "memory" and system "history/source".

## Impact

- **Systems:** Workspace Governance, Traceability, Automated CLI Scripts.
- **Documents:** `GEMINI.md`, `README.md`, `llm/folder-structure.md`, and multiple skill `SKILL.md` files.
