# Claude Cowork — Knowledge OS task templates

Versioned copy of the inbox + super-wiki scheduled tasks. **Replace placeholders** before pasting into [Claude Cowork](https://www.anthropic.com/product/claude-cowork).

## Placeholders

| Placeholder | Meaning | Example |
|-------------|---------|---------|
| `OBSIDIAN_ROOT` | Root directory containing all Obsidian vaults | `$HOME/Obsidian` |
| `OBSIDIAN_META` | Master vault path | `$HOME/Obsidian/meta` |

Skill paths of the form `~/.claude/skills/<name>/` are resolved by `skillmanager audit`. Run `skillmanager knowledge-os` afterwards to confirm the paths used in these task files are present on your machine.

## Prerequisites

All skills used by these tasks are bundled with Skillforge. Run `skillmanager audit` to install them.

| Skill path | Used by |
|------------|---------|
| `~/.claude/skills/wiki-harvest/` | Task C |
| `~/.claude/skills/super-wiki-sync/` | Tasks B, C |
| `~/.claude/skills/folder-structure-sync/` | Task B |
| `~/.claude/skills/vault-paths/` | Setup task |

## Task files

| File | Use |
|------|-----|
| [task-inbox-process.txt](task-inbox-process.txt) | Task A — inbox classification + staged move pipeline |
| [task-super-wiki-refresh.txt](task-super-wiki-refresh.txt) | Task B — super-wiki + folder-structure refresh for meta |
| [task-wiki-harvest-refresh.txt](task-wiki-harvest-refresh.txt) | Task C — wiki harvest triage: scan curated pages, surface sprint cards, chain super-wiki-sync |
| [task-vault-onboard.txt](task-vault-onboard.txt) | Setup — convert a personal vault into a governed vault (adds CLAUDE.md + _os/index.md) |

See [docs/knowledge-os.md](../../docs/knowledge-os.md) for the full architecture.
