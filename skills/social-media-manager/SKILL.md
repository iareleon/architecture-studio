---
name: social-media-manager
description: "Public-facing social and long-form content — short posts, threads, video scripts, and guides. Use when the user wants a draft for X/LinkedIn/Threads/Bluesky/Instagram, a script or shot list, a content calendar, or a how-to article — even if they only say \"make this a post\" or drop rough bullets."
metadata:
  version: "1.0"
  disable-model-invocation: true
  formerly: social-media
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
- Do not fabricate facts, statistics, or quotes. Tone and length are platform-specific (see platform references) — made-up data breaks audience trust and can have legal/brand impact.

## Routing (quick)

- Social → `workflows/social-media-posts.md`; video → `workflows/social-media-video.md`; long-form → `workflows/social-media-menu.md`.
- Read `references/platform-formats.md` for limits and format rules.

## Vault operations

Orchestrates the `social-media` Obsidian vault. Load when operating on the vault directly. Read the vault’s `CLAUDE.md` first.

| Op | Workflow |
|------|----------|
| `post` {idea} | `workflows/vault-post.md` |
| `calendar` {period} | `workflows/vault-calendar.md` |
| `promote` {slug} | `workflows/vault-promote.md` |
| `lint` | *Not in SkillsLoom yet* — `~/.claude/skills/lint/SKILL.md` if installed locally |
| `query` {question} | *Not in SkillsLoom yet* — `~/.claude/skills/query/SKILL.md` if installed locally |

Sub-skill resolution order for each :sl command:
1. `~/Obsidian/social-media/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/social-media/` — SkillsLoom default

Changelog: `references/vault-changelog-protocol.md` after any vault op that writes.
