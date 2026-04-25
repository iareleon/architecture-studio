# Memory audit workflow

Reviews durable context files for staleness, bloat, and broken references. Reports only — no writes without explicit user approval.

## Workflow

### 1. Discover files

- Glob `${SKILLFORGE_DIR}/skills/**/memory/**/*.md` (legacy; exclude `*.archived.md`)
- Glob `${SKILLFORGE_DIR}/skills/**/persona/**/*.md`
- Optional: project `CLAUDE.md` paths the user names (out-of-tree)

For each file, read the frontmatter block only (between `---` delimiters) when doing quick checks.

### 2. Run checks

**Staleness**
- If `last-updated` is older than 90 days → `STALE`

**Bloat (small memory/persona files)**
- Count non-frontmatter, non-comment lines. If &gt; 40 → `BLOATED` (suggest split or move overflow to `references/`)

**Orphan**
- File under `skills/<id>/memory/` or `.../persona/` but parent folder is not a valid skill with `SKILL.md` → `ORPHANED`

**Broken reference**
- If a skill’s `SKILL.md` has `metadata.memory-file`, the path must exist; else `BROKEN REFERENCE` (rare; field is usually omitted now)

**Persona coverage (optional)**
- If a skill has `persona/*.md` but `SKILL.md` does not mention when to load them → `UNREFERENCED PERSONA` (info)

### 3. Report

Present a summary table, for example:

```
Memory & persona audit report  (<date>)
─────────────────────────────
File                                         | Status   | Issue
---------------------------------------------|----------|------------------
skills/wiki-manager/persona/meridian.md       | OK       |
skills/legacy-skill/memory/baseline.md        | LEGACY   | No memory-file in SKILL; fold or remove
```

### 4. Propose actions

- STALE → update or confirm `last-updated`
- BLOATED → split
- ORPHANED → archive or remove
- BROKEN REFERENCE → remove `metadata.memory-file` or restore file
- LEGACY `memory/baseline` → prefer migration to `SKILL.md` + project `CLAUDE.md`

## Guidelines

- Read-only until the user approves a specific change.
- Prefer archive markers over hard deletes in sensitive notes.
