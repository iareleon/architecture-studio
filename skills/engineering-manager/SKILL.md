---
name: engineering-manager
description: "Engineering Obsidian vault — feature specs, design notes, ADRs, and promotion to the wiki. Use when the user is drafting a feature, recording a technical decision, or moving engineering material into the wiki — even if the note lives under a scratch path or a daily log first."
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# Engineering Manager

Orchestrates all engineering vault operations. Load this skill at the start of any
engineering vault session after reading the vault's `CLAUDE.md`.

**Vault:** `~/Obsidian/engineering` · **Topic focus:** architecture, specs, ADRs, system design, code decisions.

## Sub-skill Resolution Order

For each sub-skill invocation, resolve in order:
1. `~/Obsidian/engineering/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/engineering-manager/` — SkillsLoom default

## Operations

### :sl spec {feature}

Generate a feature or system specification.

1. Run spec generation for the specified feature
2. Output: `research/active/{feature-slug}-spec.md`
3. Append to `_os/log.md`: `## [date] ingest | {feature-slug}-spec`
4. Report: `Spec draft complete → research/active/{feature-slug}-spec.md`

### :sl adr {decision}

Write an architecture decision record.

1. Gather context: problem statement, options considered, constraints
2. Output: `research/active/ADR-{nn}-{decision-slug}.md`
3. Append to `_os/log.md`: `## [date] ingest | ADR-{nn}-{decision-slug}`
4. Report: `ADR draft complete → research/active/ADR-{nn}-{decision-slug}.md`

### :sl promote {slug}

Promote approved spec or ADR from `approved/` to `wiki/`.

1. Read `approved/{slug}.md` — verify `status: approved`
2. Detect type from frontmatter (`type: spec | adr | decision`)
3. Create wiki page:
   - Specs → `wiki/specs/{slug}.md`
   - ADRs → `wiki/adrs/{slug}.md`
4. Update `wiki/index.md` and top-level `index.md`
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md`
   for the wiki subfolder modified

## Changelog Protocol

After every operation, append to `_os/log.md` at the vault root:
```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```
For wiki-level operations (promote): also append to `wiki/log.md`.
