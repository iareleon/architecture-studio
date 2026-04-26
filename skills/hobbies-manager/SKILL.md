---
name: hobbies-manager
description: "Hobbies Obsidian vault — photography (shoots, reviews, technique), gear notes, and promotion to the wiki. Use when the user logs a session, rates shots, plans gear, or curates creative work into the wiki — even if the note is a quick field capture without \"hobby\" in the title."
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# Hobbies Manager

Orchestrates all hobbies vault operations. Load this skill at the start of any
hobbies vault session after reading the vault's `CLAUDE.md`.

**Vault:** `~/Obsidian/hobbies` · **Topic focus:** photography, gear, technique, camera, shoots.

## Sub-skill Resolution Order

For each sub-skill invocation, resolve in order:
1. `~/Obsidian/hobbies/.skills-override/{sub-skill-name}.md` — subscriber custom
2. `~/.claude/skills/hobbies-manager/` — SkillsLoom default

## Operations

### :sl review {shoot}

Log and review a photography shoot.

1. Read the raw shoot note from `raw/{shoot-slug}.md`
2. Extract: date, location, gear used, lighting conditions, shot list, wins, learnings
3. Output: `research/active/{shoot-slug}-review.md`
4. Append to `_os/log.md`: `## [date] ingest | {shoot-slug}-review`
5. Report: `Review drafted → research/active/{shoot-slug}-review.md`

### :sl promote {slug}

Promote an approved shoot review or gear note from `approved/` to `wiki/`.

1. Read `approved/{slug}.md` — verify `status: approved`
2. Detect type from frontmatter (`type: shoot | gear | technique`)
3. Create wiki page:
   - Shoot reviews → `wiki/shoots/{slug}.md`
   - Gear notes → `wiki/gear/{slug}.md`
   - Technique notes → `wiki/technique/{slug}.md`
4. Update `wiki/index.md` and top-level `index.md`
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md`
   for the wiki subfolder modified (`wiki/shoots/`, `wiki/gear/`, or `wiki/technique/`)

## Changelog Protocol

After every operation, append to `_os/log.md` at the vault root:
```
## [YYYY-MM-DD] {op} | {slug}
{one-line description of what was done}
```
For wiki-level operations (promote): also append to `wiki/log.md`.
