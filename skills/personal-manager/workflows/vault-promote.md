# Vault :sl promote {slug}

Promote an approved reflection from `approved/` to `wiki/` in the `personal` Obsidian vault. Read the vault’s `CLAUDE.md` first.

1. Read `approved/{slug}.md` — verify `status: approved`
2. Detect type from frontmatter (`type: reflection | goal | milestone`)
3. Create wiki page:
   - Reflections → `wiki/reflections/{slug}.md`
   - Goals → `wiki/goals/{slug}.md`
   - Milestones → `wiki/milestones/{slug}.md`
4. Update `wiki/index.md` and top-level `index.md`
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md` for the wiki subfolder modified

Afterward: `references/vault-changelog-protocol.md` for the full log format.
