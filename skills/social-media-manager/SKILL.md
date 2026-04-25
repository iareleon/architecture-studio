---
name: social-media-manager
description: Published social and long-form content — router for social posts, video scripts, and guides. Invoke for posts, scripts, or articles.
metadata:
  version: "1.0"
  disable-model-invocation: true
---
# Social media (router)

**Main brain:** this file. Brand voice, platforms, and equipment for *your* setup belong in project `CLAUDE.md` or a named project doc—do not require a per-skill `memory/baseline.md`.

**Menu and long-form:** `workflows/social-media-menu.md`. Platform formats: `references/platform-formats.md`.

| Type | Workflow |
|------|----------|
| Social post (X, LinkedIn, Instagram, Threads, Bluesky) | `workflows/social-media-posts.md` |
| Video / script / shot list | `workflows/social-media-video.md` |
| Written guide, blog, how-to | `workflows/social-media-menu.md` (or inline in menu) |

## Approval and honesty

- Propose outline or structure before full draft.
- **One** piece at a time—no bundling without separate approvals.
- Never fabricate facts, statistics, or quotes. Tone and length are platform-specific (see platform references).

## Routing (quick)

- Social → `workflows/social-media-posts.md`; video → `workflows/social-media-video.md`; long-form → `workflows/social-media-menu.md`.
- Read `references/platform-formats.md` for limits and format rules.

## Vault Operations

Orchestrates the `social-media` Obsidian vault. Load this section when operating on the vault directly. Read the vault's `CLAUDE.md` before running any op.

Sub-skill resolution order for each op:
1. `~/Obsidian/social-media/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/social-media/` — Skillforge default

### op: post {idea}

Draft a platform-specific post from a raw idea or capture.

1. Read the raw idea from `raw/{idea-slug}.md` or inline content
2. Identify target platform (LinkedIn, Instagram, X, etc.) from frontmatter or prompt
3. Draft post in the platform's native format and voice — see `references/platform-formats.md`
4. Output: `research/active/{YYYYMMDD}-{platform}-{idea-slug}.md`
5. Append to `_os/log.md`: `## [date] ingest | {platform}-{idea-slug}`
6. Report: `Post drafted → research/active/{YYYYMMDD}-{platform}-{idea-slug}.md`
<!-- sub-skill: workflows/post-generator.md — not yet authored -->

### op: calendar {period}

Generate or update a content calendar for a given period (e.g. `2026-05`).

1. Read all approved posts in `approved/` not yet assigned to a calendar slot
2. Read existing calendar file if present: `wiki/calendar/{period}.md`
3. Assign or suggest post slots across the period by platform and cadence
4. Output: `wiki/calendar/{period}.md` (create or update)
5. Append to `_os/log.md`: `## [date] calendar | {period}`
6. Report: `Calendar updated → wiki/calendar/{period}.md`
<!-- sub-skill: workflows/content-calendar.md — not yet authored -->

### op: promote {slug}

Promote an approved post from `approved/` to `wiki/`.

1. Read `approved/{slug}.md` — verify `status: approved`
2. Detect platform from frontmatter
3. Create wiki page: `wiki/posts/{slug}.md`
4. Update `wiki/index.md` and top-level `index.md`
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md`
   for `wiki/posts/` and `wiki/calendar/` (if modified)

### op: lint

<!-- sub-skill: ~/.claude/skills/lint/SKILL.md — not yet in Skillforge -->

### op: query {question}

<!-- sub-skill: ~/.claude/skills/query/SKILL.md — not yet in Skillforge -->

## Changelog Protocol (vault)

After every vault operation, append to `_os/log.md` at the vault root:
```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```
For wiki-level operations (promote, calendar): also append to `wiki/log.md`.
