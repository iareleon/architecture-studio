# Skills Audit Subflow

Audits skill content quality — frontmatter correctness, lean structure, and memory
file health. Symlink and state invariant issues are delegated to the `skillmanager` CLI.

## Workflow

### 1. Discover Skills

Use Glob with `${SKILLSLOOM_DIR}/skills/**/SKILL.md` excluding `workflows/`, or scan active and lifecycle dirs. The parent folder name is the skill id (kebab-case).

### 2. Run Checks

Read each `SKILL.md` and collect all failures before reporting. Run every check
regardless of earlier failures.

**Naming convention checks:**
- Directory base name is not valid kebab-case or is reserved (`review`, `deactivated`, etc.) → `NAMING VIOLATION`

**Frontmatter checks:**
- `name` field value does not match directory name → `NAME MISMATCH`
- `description` field is absent or empty → `MISSING DESCRIPTION`
- `disable-model-invocation: true` absent → `MISSING DMI FLAG`
- `metadata.memory-file` if **present** must resolve to an existing file → `BROKEN MEMORY-FILE REFERENCE` if path missing (field is **optional** — most skills use `SKILL.md` + `persona/` only)

**Lean checks:**
- Any contiguous block of non-heading, non-code prose exceeds 10 lines → `BLOATED SECTION` (flag the heading)
- Long lists, lookup tables, or embedded specs present with no `## References` section → `MISSING REFERENCES SECTION`

**Memory / legacy checks:**
- If `metadata.memory-file` is set, the file must exist at the given path; else → `BROKEN MEMORY-FILE REFERENCE`
- `skills/<id>/memory/**/*.md` without `metadata.memory-file` in that skill’s `SKILL.md` → `LEGACY MEMORY FILE` (info — candidate to fold into `SKILL.md` or project `CLAUDE.md`)
- For any remaining per-skill memory file: `last-updated` older than 90 days → `STALE` (suggest review)
- Optional: `persona/**/*.md` should be referenced from the parent `SKILL.md` router or be obviously standalone — flag `UNREFERENCED PERSONA` if a skill has a `persona/` tree but no table row (warn only)

**Deferred skill checks:**
- Use Glob `${SKILLSLOOM_DIR}/skills/skill-manager/references/deferred-skill-plans/*.md`
- For each, read the `deferred-on` frontmatter field
- If older than 30 days → `DEFERRED SKILL OVERDUE: <skill-name>`

### 3. Delegate State Issues

Do not attempt to fix symlinks or rename directories. After presenting the report:

```
For state and validation violations, run: skillmanager audit
```

### 4. Report

Present a full summary table:

```
Skill           | Check                        | Status
--------------- | ---------------------------- | ------
```

Flag content and memory issues for manual review. Do not auto-edit skill bodies
or memory files.

## Guidelines

- Read-only — this subflow never writes files.
- Invariant enforcement belongs exclusively to `skillmanager audit`.
- Surface deferred skill reminders as informational — do not block the report on them.
