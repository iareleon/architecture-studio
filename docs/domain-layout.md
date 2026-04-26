---
title: Domain (skill) layout — research and standard
---

# Domain layout — research and approved standard

A **domain** in SkillsLoom is one activatable unit: the directory `skills/<skill-id>/`. Visibility to the LLM is controlled by `metadata.status` in `SKILL.md`, not by moving folders. A domain must stay **self-contained**: everything specific to that domain lives under its tree, with **single responsibility** per file and no duplicated facts across skills.

## Research summary (industry practice)

- **Progressive disclosure** (Anthropic Agent Skills: [Authoring best practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)): `SKILL.md` is the entry and table of contents; long material is split so only what is needed is loaded. Bodies of supporting docs stay in sibling files, not in one giant `SKILL.md` (practical limit: keep `SKILL.md` on the order of hundreds of lines, not thousands).
- **Shallow structure**: Reference files are linked **one level** under the skill (e.g. `references/topic.md`, `workflows/commit.md`) so routers can point to a stable path without deep nesting.
- **Separation of concerns**: Executable tooling lives in `scripts/` (code), procedural steps in `workflows/` (markdown), durable preferences in `memory/`, static facts in `references/`, fill-in scaffolds in `templates/`.
- **Composability**: Multiple small skills with clear `description` triggers compose better than one monolith. Cross-domain behaviour is achieved by **delegation** and **links**, not by copying content.

## Approved directory shape

Every domain (skill) **may** use these top-level children — create only what you need; omit empty folders.

| Path (under `skills/<id>/`) | Single responsibility | Notes |
|----------------------------|------------------------|--------|
| `SKILL.md` | Router: when to use the skill, how to load other files, delegation table | Required. |
| `workflows/` | Procedural / step-by-step markdown (menus, “run this flow”) | Optional. One file = one workflow. |
| `memory/` | **Legacy** optional notes beside a skill; avoid for new work — use project `CLAUDE.md` and `persona/` instead | If present, may still be named in `metadata.memory-file` (rare). |
| `templates/` | Scaffolds the model fills in (outlines, forms) | Optional. |
| `scripts/` | Deterministic code (executed, not “read for prose”) | Optional. |
| `references/` | Stable facts, tables, checklists, lazy-loaded read models | Optional. |
| `persona/` | Distinct sub-topic **within** one skill (e.g. Python vs React) — one file per persona; load only when that stack applies | Optional. Prefer this over bloating `SKILL.md` when subject matter is clearly separate. |
| `context.md` | Auto-generated index (e.g. workflow list) | Optional; may be produced by `skillmanager audit`. |

### Naming rules

- **Folders** are plural where they hold a set: `workflows/`, `references/`, `templates/`, `persona/`, `memory/` (legacy), `scripts/`.
- **Filenames** use **kebab-case** and describe **content or intent**, not file format or “role in repo”.
  - **Do not** encode role in the *stem* of the name: avoid `-sf`, `-wf`, `-sme`, `-ref` (the **directory** already encodes the role: `workflows/`, `references/`, …).
- **Markdown** uses a single extension: `.md`. That is a transport convention, not a “content tag”; it is always required for normal tooling.
- **Templates** that are meant to be copied and filled: use a **second marker** before the extension, e.g. `adr.template.md` or `hld-section.template.md`, so the name stays a normal phrase plus `.md`.
- **Scripts** are an **exception** to “no type suffix in the *stem*”; the **language** must be visible for the OS and shebang (`script-name.py`, `script-name.sh`, `script-name.bash`, …). Prefer one obvious extension per file.

## Skill dependencies (no duplication)

- **No duplicate copy** of another domain’s reference text: if `git` and `cloud-engineer` both need the same long fact, it belongs in **one** owning domain (or a small shared `references/` under the skill that *owns* that fact) and other skills must **link** to it (path from repo root) or **delegate** (“invoke the `cloud-engineer` skill for project inventory”).
- Use `metadata.related-skills: [other-skill, …]` in `SKILL.md` to declare coordination; routers should say *when* to hand off, not re-explain the other domain.
- `../other-skill/references/...` from within the repo is fine for human-readable pointers; the model should still prefer **explicit delegation** in prose when a whole workflow belongs to another skill.

## Migration note (this repo)

Previously this repository used a `subflows/` directory, `*-sf.md` filenames, and a single `memory.md` at the domain root. The current standard uses **`workflows/`**, **neutral** workflow filenames, **`SKILL.md` as the main brain** for each skill, and optional **`persona/`** for clearly distinct sub-topics. Per-skill **`memory/baseline.md`** is legacy—prefer project-level notes and `persona/<topic>.md` for new content.
