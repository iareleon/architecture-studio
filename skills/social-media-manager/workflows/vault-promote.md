# Vault :sl promote {slug}

Promote an approved post from `approved/` to `wiki/` in the `social-media` Obsidian vault. Read the vault’s `CLAUDE.md` first.

1. Read `approved/{slug}.md` — verify `status: approved`
2. Detect platform from frontmatter
3. Create wiki page: `wiki/posts/{slug}.md`
4. Update `wiki/index.md` and top-level `index.md`
5. Append to `wiki/log.md` and `_os/log.md`
6. Run folder-structure-sync via `~/.claude/skills/wiki-manager/workflows/folder-structure-sync.md` for `wiki/posts/` and `wiki/calendar/` (if modified)

Afterward: `references/vault-changelog-protocol.md`.
