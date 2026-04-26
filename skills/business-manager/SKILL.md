---
name: business-manager
description: "Business Obsidian vault — strategy research, market/competitive notes, client briefs, and promotion to the wiki. Use when the user is capturing deals, writing positioning, building a case, or needs anything promoted from the business vault — even if they call it a \"work note\" or a \"meeting follow-up.\""
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# Business Manager

Orchestrates all business vault operations. Load this skill at the start of any
business vault session after reading the vault's `CLAUDE.md`.

**Vault:** `~/Obsidian/business` · **Topic focus:** clients, strategy, business decisions, revenue, consulting.

## Sub-skill Resolution Order

For each sub-skill invocation, resolve in order:
1. `~/Obsidian/business/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/business-manager/` — SkillsLoom default

## Operations

### :sl research {topic}

Research a business strategy topic or decision.

1. Run strategy research on the specified topic
2. Output: `research/active/{topic-slug}.md`
3. Append to `_os/log.md`: `## [date] ingest | {topic-slug}`
4. Report: `Research complete → research/active/{topic-slug}.md`

### :sl brief {client}

Generate or update a client engagement brief.

1. Check `wiki/clients/` for an existing brief matching the client slug
2. If new: gather context (client name, engagement type, goals, constraints,
   timeline, key contacts) and create `research/active/{client-slug}-brief.md`
3. If update: read existing wiki brief and draft updated sections only
4. Set `status: researched`
5. Append to `_os/log.md`: `## [date] ingest | {client-slug}-brief`
6. Report: `Brief drafted → research/active/{client-slug}-brief.md`

### :sl promote {slug}

Promote approved research or brief from `approved/` to `wiki/`.

1. Read `approved/{slug}.md` — verify `status: approved`
2. Detect type from frontmatter (`type: strategy | brief | decision`)
3. Create wiki page:
   - Strategy → `wiki/strategy/{slug}.md`
   - Client briefs → `wiki/clients/{slug}.md`
   - Decisions → `wiki/decisions/{slug}.md`
4. Update `wiki/index.md` and top-level `index.md`
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md`
   for the wiki subfolder modified (`wiki/strategy/`, `wiki/clients/`, or `wiki/decisions/`)

## Changelog Protocol

After every operation, append to `_os/log.md` at the vault root:
```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```
For wiki-level operations (promote): also append to `wiki/log.md`.
