# Review One Skill (need + efficiency)

Systematically review a **single** skill to decide if it is still needed and whether personas, references, and the router are **token-efficient**. Use this when you are going through the catalog one skill at a time—not for repo-wide batch audits (see `skills-audit.md`).

## When to use

- You want a **go/no-go** on keeping, merging, or retiring a skill.
- You are checking **persona/** and **references/** for duplication, missing router links, or bloat.
- You are applying the principles in the parent `SKILL.md` **Design principles (token, cost, and shape)**.

## Workflow

### 1. Select the skill

Confirm folder `skills/<name>/` and read `SKILL.md` in full. Optionally run `skillmanager ls` to see the published `description`.

Glob and list (do not read every file yet):

- `persona/**/*.md` (if any)
- `references/**/*.md` (if any)
- `workflows/**/*.md` (if any)

### 2. Need (purpose)

| Question | Pass criteria |
|----------|----------------|
| **Distinct role?** | The `description` names **when** to invoke; no other active skill fully subsumes this role. |
| **Overlap?** | If another skill is ~the same, plan **merge** or set `metadata.related-skills` and one primary skill—see parent `SKILL.md` design principles. |
| **Obsolescence?** | If the domain is gone or replaced by tools/docs elsewhere, plan **`deactivated`** or **`decommissioned`** + `skillmanager audit`, not a bloated “legacy” body. |

Record: **keep / merge / retire** (and merge target or retirement reason if applicable).

### 3. Router efficiency (`SKILL.md`)

| Question | Pass criteria |
|----------|----------------|
| **Router vs manual?** | Short routing table or bullets; no multi-screen prose. Align with `skills-refine.md` (lean `SKILL.md`) and `skills-audit.md` (no bloated sections). |
| **Lazy load design?** | The reader can pick **one** next file from the router for the current task. |
| **Deduplication?** | Long lists, templates, and command matrices live in `references/` or `workflows/`, not repeated in the router. |

### 4. Personas

Skip this section if `persona/` is absent.

| Question | Pass criteria |
|----------|----------------|
| **Justified split?** | Each persona file is an **orthogonal** subject (e.g. different stack); not a random slice of the same short doc. |
| **Router index?** | Every `persona/*.md` appears in a **When to load** (or equivalent) table in `SKILL.md`—per `skills-audit.md` **UNREFERENCED PERSONA** guidance. |
| **Minimum files?** | No explosion of tiny personas; merge thin files or fold shared lines into `references/`. |

### 5. References

| Question | Pass criteria |
|----------|----------------|
| **Exist and resolve?** | Every `references/` path from `SKILL.md` exists. |
| **When-to-load?** | Router or workflow states **when** to read each file (task or symptom), not a dump of all refs up front. |
| **One topic (or clear sections)?** | Prefer focused files; if one file is huge, consider splitting by subtopic. |

### 6. Outcome and next steps

Summarize in a short table:

```
Skill: <name>
Decision: keep | merge into <x> | retire (<status>)
SKILL.md: pass | needs slimming
Personas: N/A | pass | needs merge / index
References: pass | fix broken links / split / dedupe
```

- If edits are required → follow `skills-refine.md` (user approval for writes), then `Run: skillmanager audit`.
- If only informational → no file write.

## Guidelines

- Read-only review unless the user or `skills-refine` explicitly approves changes.
- Canonical schema remains `docs/skill-spec.md`; this workflow does not override repository validation or `skillmanager audit`.
