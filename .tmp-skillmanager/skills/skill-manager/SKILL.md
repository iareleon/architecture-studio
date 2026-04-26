---
name: skill-manager
description: Create, audit, and lifecycle-manage skills under skills/. Invoke when creating, reviewing, refining, detecting, or auditing any skill.
metadata:
  version: "2.0"
  disable-model-invocation: true
---
# Skill Manager

**Single responsibility:** create, list, audit, and lifecycle-manage **skills** under `skills/` with the `skillmanager` CLI. Memory edits → `brain-manager` skill. Knowledge base routing → `vault-paths` or your configured knowledge base skill.

## Global Rule — applies to every skill and agent

> **No skill or agent may take any action unless confidence ≥ 95% AND the user has explicitly approved.**

- If confidence < 95%: state the uncertainty, present options, ask for guidance. **Never guess or invent.**
- Every consequential action (write, delete, rename, audit) requires explicit user sign-off before execution.
- **Human in the loop is non-negotiable.** Skills amplify human capability — they do not replace human judgement. The human always has the final say.
- When advising on best practices, distinguish clearly between known convention and personal recommendation.

## Routing

| Intent | Workflow |
|--------|----------|
| List / discover skills | `workflows/skill-manager-menu.md` — `skillmanager ls` |
| Review one skill (need, personas, references, token budget) | `workflows/skills-review-one.md` |
| Create / scaffold | `workflows/skills-create.md` |
| Detect gaps | `workflows/skills-detect.md` |
| Audit (repo-wide quality) | `workflows/skills-audit.md` |
| Propose to repo | `workflows/skills-propose.md` |
| Refine (edit after diagnosis) | `workflows/skills-refine.md` |

## Design principles

- **Router-first:** `SKILL.md` is a routing table — push depth to `references/`, procedures to `workflows/`.
- **Lazy load:** Follow one link per turn. Do not read the full `workflows/` or `references/` tree up front.
- **Single responsibility:** One clear, non-overlapping role per skill. Merge near-duplicates; retire obsolete skills.
- **Token budget:** No large inline blocks in `SKILL.md`. Overflow → `references/`.
- **Personas (`persona/`):** Use only for orthogonal subjects. One file = one load condition.

## Conventions

- New skills only under `${SKILLSLOOM_DIR}/skills/<name>/`; directory name = kebab-case; `name:` in frontmatter must match.
- Set `metadata.status` in `SKILL.md` (default `active`); run `skillmanager audit` to update symlinks.
- After authoring: `Run: skillmanager audit`.
- No personal data, paths, or credentials in any SKILL.md.
- **Templates:** `templates/expertise-skill-template.md`, `templates/workflow-skill-template.md`.
- Skill names must not shadow LLM built-in commands or native capabilities (e.g. `memory`, `browser`, `search`). Before finalising a name, check `references/marketplace-overlap.md` and run `skillmanager ls`; rename before activation if a conflict is found.

CLI and subflow details: `workflows/skill-manager-menu.md`.
