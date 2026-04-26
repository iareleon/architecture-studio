---
name: product-manager
description: "Product Obsidian vault — idea research, viability, competitive framing, design imports, and promotion to the wiki. Use when the user is shaping a bet, a PRD sketch, a customer problem, or moving product thinking into the wiki — even if the file is a rough note in `raw/` with no product jargon."
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# Product Manager

Orchestrates all product vault operations. Load this skill at the start of any
product vault session after reading the vault's `CLAUDE.md`.

**Vault:** `~/Obsidian/product` · **Topic focus:** product ideas, features, market thinking, startup concepts.

## Sub-skill Resolution Order

For each sub-skill invocation, resolve in order:
1. `~/Obsidian/product/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/product-manager/` — SkillsLoom default

## Operations

### :sl research {idea}

Research a product idea or concept.

1. Run product research on the specified idea
2. Output: `research/active/{idea-slug}.md`
3. Append to `_os/log.md`: `## [date] ingest | {idea-slug}`
4. Report: `Research complete → research/active/{idea-slug}.md`

### :sl viability {idea}

Run a full viability assessment on a researched idea.

1. Verify `research/active/{idea-slug}.md` or `approved/{idea-slug}.md` exists
2. Assess market size, revenue model, unit economics (financial viability)
3. Assess build complexity, stack fit, risk (technical viability)
4. Output: append viability sections to the research file or create
   `research/active/{idea-slug}-viability.md`
5. Set `status: viability-assessed`
6. Append to `_os/log.md`: `## [date] viability | {idea-slug}`

### :sl design-import {raw-file}

Import a Claude design artifact from `raw/` and convert it to a structured spec.

1. Load `workflows/design-import.md`
2. Run design import on `raw/{raw-file}.md`
3. Output: `research/active/{idea-slug}-design-spec.md`
4. Append to `_os/log.md`: `## [date] design-import | {idea-slug}`
5. Report: `Design spec complete → research/active/{idea-slug}-design-spec.md`

### :sl promote {idea}

Promote an approved idea from `approved/` to `wiki/`.

1. Read `approved/{idea-slug}.md` — verify `status: approved`
2. Create wiki pages:
   - `wiki/concepts/{idea-slug}.md` — full research and viability summary
   - Any new `wiki/viability/{idea-slug}-assessment.md` if viability was run
   - Any new `wiki/competitive/{idea-slug}-landscape.md` if competitive research exists
3. Update `wiki/index.md` — add new pages under correct sections
4. Update top-level `index.md` — add link to new concept page
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md`
   for each folder modified (e.g. `wiki/concepts/`, `wiki/viability/`, `wiki/competitive/`)

## Changelog Protocol

After every operation, append to `_os/log.md` at the vault root:
```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```
For wiki-level operations (promote): also append to `wiki/log.md`.
