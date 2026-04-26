# Wiki harvest — meta (Knowledge OS) install context

Load when the user is working in the **meta** master vault or when routing targets the Knowledge OS **inbox** / **super-wiki** pipeline. General process is in `../SKILL.md`. For **product wiki pages in Meridian (arch-agency)**, use `meridian.md` instead.

## System paths (example install)

- Meta vault: `~/Obsidian/meta` (override with `OBSIDIAN_META`)
- Per-vault registry pages (auto): `~/Obsidian/meta/wiki/{vault-id}.md` — produced by `super-wiki-sync` from each vault’s `_os/log.md` / index. **Do not treat these as hand-written wiki pages.**
- Domain / scope pages in **meta** (curated): `~/Obsidian/meta/wiki/*.md` that describe *domains* (e.g. business, product) are **narrative**; they are not the same as the per-vault `{vault}.md` rows. When unclear, read `meta/_os/index.md` and `meta/CLAUDE.md` first.
- Inbox: `~/Obsidian/meta/inbox/`
- Global index: `~/Obsidian/_super-wiki.md` (auto)
- Ingestion log: `~/Obsidian/meta/inbox/.classify.log` (if present)

## When **not** to use Meridian page schema

[references/wiki-page-schema.md](../references/wiki-page-schema.md) (vision, architecture, ADRs) applies to **arch-agency** and similar *product* wikis. For **meta** registry files and auto-generated `meta/wiki/{vault}.md`, follow the `super-wiki-sync` and `inbox-classifier` op-skills—do not impose 🟡/🟠/🟢 on machine-generated index rows.

For **curated** domain pages under `meta/wiki/` where the user runs a brain-dump, you *may* reuse the same status emoji pattern **only if** the user has already adopted it on that page; otherwise use the page’s existing frontmatter and sections.

## Chaining

After moves from inbox: `folder-structure-sync` (destination) → `super-wiki-sync`. Never hand-edit `meta/_os/index.md` or auto-generated per-vault registry pages unless the op-skill says so.

## See also

- [docs/knowledge-os.md](../../../docs/knowledge-os.md) in the SkillsLoom repo
- [vault-paths/references/vault-map.md](../../vault-paths/references/vault-map.md) — `meta` row
