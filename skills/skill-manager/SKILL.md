---
name: skill-manager
description: Create, audit, refine, and lifecycle-manage skills under skills/. Use this skill whenever the user wants to create a new skill, scaffold a SKILL.md, capture a repeatable workflow as a skill, check whether a skill exists for a task, review or improve an existing skill, detect gaps in the skill library, audit skill quality or naming, propose a skill to the repository, or asks anything like "can you make a skill for this?", "do I have a skill that does X?", "review my skills", or "let's improve this skill". Trigger even when the user describes a workflow they want to automate — that's a skill creation opportunity.
metadata:
  version: "2.1"
  disable-model-invocation: true
---
# Skill Manager

**Single responsibility:** create, list, audit, and lifecycle-manage **skills** under `skills/` with the `skillmanager` CLI. Memory edits → `brain-manager` skill. Knowledge base routing → `wiki-manager` or your configured knowledge base skill.

## Working principles

Skills get loaded into every future conversation that triggers them — a mistake baked into a skill propagates to every subsequent use. For this reason, confirm intent before writing or deleting anything, surface uncertainty rather than guessing, and present options when more than one valid path exists. Distinguish personal recommendation from established convention when advising on best practices.

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
