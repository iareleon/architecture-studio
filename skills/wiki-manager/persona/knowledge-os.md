# Wiki Manager — meta (Knowledge OS) install context

Load when working in the **meta** master vault or when running inbox / super-wiki operations. For product wiki sessions in **arch-agency (Meridian)**, load `meridian.md` instead.

## System paths

- Meta vault: `{OBSIDIAN_META}` (set in terminal environment)
- Config: `{OBSIDIAN_META}/wiki-manager.config.yaml`
- Per-vault registry pages (auto-generated): `{OBSIDIAN_META}/wiki/{vault-id}.md` — written by `wiki-sync`. **Do not treat these as curated wiki pages.**
- Curated domain pages: `{OBSIDIAN_META}/wiki/*.md` that describe domains (e.g. business, product) — these are narrative and hand-maintained.
- Inbox: `{OBSIDIAN_META}/inbox/` (subfolders: `raw/`, `review/`, `approved/`)
- Global index: `{obsidian_root}/_super-wiki.md` (auto-generated)

When unclear whether a page is curated or auto-generated: read `{OBSIDIAN_META}/_os/index.md` and `{OBSIDIAN_META}/CLAUDE.md` first.

## When NOT to use wiki-page-schema.md status emojis

`references/wiki-page-schema.md` (🟡/🟠/🟢/🚀 status ladder) applies to **curated narrative wiki pages**.

Do NOT apply it to:
- Auto-generated per-vault registry files (`{OBSIDIAN_META}/wiki/{vault-id}.md`)
- Auto-generated index files (`_super-wiki.md`, `_os/index.md`, `_structure.md`)

For curated domain pages under `{OBSIDIAN_META}/wiki/` where the user runs a brain dump: use the status emoji pattern only if the user has already adopted it on that page.

## Chaining after inbox moves

After `inbox-dispatch` or `vault-inbox-sync`: run `folder-structure-sync.md` for the destination folder, then `wiki-sync.md`. Never hand-edit `{OBSIDIAN_META}/_os/index.md` or auto-generated per-vault registry pages.

## See also

- `references/config-schema.md` — full config.yaml field reference
- [docs/knowledge-os.md](../../../docs/knowledge-os.md) in the SkillsLoom repo
