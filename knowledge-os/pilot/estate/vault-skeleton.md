# Vault layout — estate agency pilot (example)

Use `~/Obsidian` as `OBSIDIAN_ROOT`. Adjust names to your client; keep **one meta vault** per machine org.

## `meta/` (master)

- `CLAUDE.md` — from your Knowledge OS template; states generated files policy.
- `_os/index.md`, `_os/_structure.md`, `_os/log.md` — as per your `super-wiki-sync` / `folder-structure-sync` op-skills.
- `inbox/` — only entry point for unclassified capture (routes into domain vaults after approval).
- `wiki/business.md` (optional curated page) — *scope* of how this client uses the OS; not the per-vault registry row.
- `wiki/property-ops.md` (optional) — SOPs that apply across the org.

**Do not** confuse **curated** `meta/wiki/*.md` with **`meta/wiki/{vault}.md`** machine-generated per-vault registry pages.

## `listings/` (example domain vault)

Single line-of-business vault (could be `lettings` or `sales` per brand).

- `CLAUDE.md` — domain-specific loading rules.
- `_os/index.md` — local registry; feeds super-wiki.
- `raw/` — property briefs, viewing notes, photos metadata (as markdown).
- `wiki/` — promoted, reviewed pages (templates, checklists, comparables).
- `research/` — optional staging before wiki promotion (match your product pipeline if used).

## Git (optional but recommended for teams)

- One private repo per org or per vault; `skillmanager git` for conventional commits.
- Branches for draft vs main wiki—keep policy in `CLAUDE.md`.
