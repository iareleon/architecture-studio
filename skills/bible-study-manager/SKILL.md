---
name: bible-study-manager
description: "Bible-study Obsidian vault — passage research, cross-references, theme synthesis, study guides, and promotion to the wiki. Use when the user wants to work a passage, build a study outline, track themes, prep teaching notes, or move notes from raw to wiki — even if they only say things like \"I read this in Romans\" or \"help me turn this into a study.\""
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# Bible-Study Manager

Orchestrates all bible-study operations. Load this skill at the start of any
bible-study vault session after reading the vault's `CLAUDE.md`.

**Vault:** `~/Obsidian/bible-study` · **Topic focus:** Bible passages, scripture, theology, exegesis, study notes.

## Sub-skill Resolution Order

For each sub-skill invocation, resolve in order:
1. `~/Obsidian/bible-study/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/bible-study-manager/` — SkillsLoom default

## Operations

### :sl research {cluster}

Research a passage cluster (e.g. `genesis-1-3`).

1. Load `workflows/passage-research.md`
2. Run passage-research on the specified cluster
3. Output: `research/active/{cluster-slug}.md`
4. Append to `_os/log.md`: `## [date] ingest | {cluster-slug}`
5. Report: `Research complete → research/active/{cluster-slug}.md`

### :sl promote {cluster}

Promote an approved cluster from `approved/` to `wiki/`.

1. Read `approved/{cluster-slug}.md` — verify `status: approved`
2. Load `workflows/passage-research.md` to understand output format
3. Create wiki pages:
   - `wiki/passages/{cluster-slug}.md` — full study guide
   - Any new `wiki/themes/{theme-slug}.md` pages identified
   - Any new `wiki/people/{person-slug}.md` pages identified
4. Update `wiki/index.md` — add new pages under correct sections
5. Update top-level `index.md` — add link to new passage page
6. Append to `wiki/log.md` and `_os/log.md`
7. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md`
   for each folder modified: `wiki/passages/`, `wiki/themes/`, `wiki/people/` (as applicable)

### :sl theme-synthesis

Synthesise themes across 3+ approved passage clusters.

1. Read all `wiki/passages/` and `wiki/themes/` pages
2. Identify cross-passage theme patterns
3. Update or create `wiki/themes/*.md` pages
4. Update `wiki/index.md` Themes section

### :sl study-guide {cluster}

Generate a formatted study guide from a promoted wiki passage.

1. Read `wiki/passages/{cluster-slug}.md`
2. Read `raw/templates/study_guide_template.md` for format reference
3. Produce `wiki/passages/{cluster-slug}-study-guide.md`

## Changelog Protocol

After every operation, append to `_os/log.md` at the vault root:
```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```
For wiki-level operations (promote, theme-synthesis): also append to `wiki/log.md`.

## ADR Flags

- ADR-02: Passage granularity — this skill assumes narrative clusters (e.g. Gen 1–3 together).
  If atomic per-chapter is preferred, update the `:sl research` step 2.
