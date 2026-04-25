# Claude Cowork — Knowledge OS task templates

Versioned copy of the inbox + super-wiki scheduled tasks. **Replace placeholders** before pasting into [Claude Cowork](https://www.anthropic.com/product/claude-cowork).

## Placeholders

| Placeholder | Meaning | Example |
|-------------|---------|---------|
| `OBSIDIAN_ROOT` | Root directory containing all Obsidian vaults | `$HOME/Obsidian` |
| `OBSIDIAN_META` | Master vault path | `$HOME/Obsidian/meta` |

Skill paths of the form `~/.claude/skills/<name>/` are resolved by `skillmanager audit`. Run `skillmanager knowledge-os` afterwards to confirm the paths used in these task files are present on your machine.

## Prerequisites

Each task depends on skills that are **not bundled with Skillforge** (marked `choreokit` below). Install them separately and ensure they are symlinked into `~/.claude/skills/`:

| Skill path | Source | Used by |
|------------|--------|---------|
| `~/.claude/skills/classify/` | choreokit / Knowledge OS op-skills | Task A |
| `~/.claude/skills/core/` (super-wiki-sync, folder-structure-sync) | choreokit / Knowledge OS op-skills | Tasks A, B, C |
| `~/.claude/skills/wiki-harvest/` | **Skillforge** (`skillmanager audit`) | Task C |

## Task files

| File | Use |
|------|-----|
| [task-inbox-process.txt](task-inbox-process.txt) | Task A — inbox classification + process-inbox |
| [task-super-wiki-refresh.txt](task-super-wiki-refresh.txt) | Task B — super-wiki + folder-structure refresh for meta |
| [task-wiki-harvest-refresh.txt](task-wiki-harvest-refresh.txt) | Task C — wiki harvest triage: scan curated pages, surface sprint cards, chain super-wiki-sync |

See [docs/knowledge-os.md](../../docs/knowledge-os.md) for the full architecture.
