# Memory create workflow

Scaffolds a new **durable context** file for the user (project, persona, or legacy skill memory).

## Workflow

### 1. Classify the target

Ask what to create:

- **A)** Project / workspace file (e.g. `CLAUDE.md` at repo root) — *preferred* for product and team context  
- **B)** Per-skill **persona** (e.g. `skills/<skill>/persona/<topic>.md`) for a narrow sub-topic (Python vs React, Meridian install, …)  
- **C)** Legacy `skills/<skill>/memory/baseline.md` only if the user still wants a separate memory layer next to a skill (discouraged for new work)

### 2. If persona (B)

- Confirm skill id and a short `kebab-case` filename (e.g. `local-overrides`, `meridian`, `python`).
- Default path: `${SKILLFORGE_DIR}/skills/<skill-id>/persona/<name>.md` (create `persona/` if needed).
- Add a one-line load hint in the parent skill’s `SKILL.md` (router table) if it does not already list this file.

### 3. If project (A)

- Default path: workspace root `CLAUDE.md` (or path the user names).
- Do **not** silently overwrite; propose stub content in a diff first.

### 4. If legacy (C)

- Path: `${SKILLFORGE_DIR}/skills/<name>/memory/baseline.md` (create `memory/` if needed). Prefer (A) or (B) instead for new work.

### 5. Choose a scaffold (style hint)

- Expertise / SME tone → `references/scaffold-sme.md`
- Workflow / ops tone → `references/scaffold-workflow.md`
- Short shared preface: `references/scaffold-shared.md` (rare)

### 6. Propose the stub (example)

Show content and path:

```
Target: <full path from above>
---
skill: <optional>
last-updated: <today>
---
<!-- Bullet facts, max ~40 lines in small files. -->

Create this file? (yes / cancel)
```

### 7. Write on approval

- Create parent directories as needed. Confirm: `Memory stub created: <path>`.

## Guidelines

- Never overwrite without the normal update + approval flow.
- Encourage project `CLAUDE.md` and `persona/<topic>.md` over new `memory/baseline.md`.
