# Wiki Manager Config

Creates or updates `wiki-manager.config.yaml` in `OBSIDIAN_META`. Run once after install and whenever vaults or routing rules change.

## Step 1 — Check for existing config

Check if `{OBSIDIAN_META}/wiki-manager.config.yaml` exists.

- If it exists: read it and display current values. Ask: "What would you like to change? (paths / routing / vaults / all)"
- If it does not exist: proceed to Step 2.

## Step 2 — Collect install paths

Ask:

```
What is your Obsidian root path? (e.g. ~/Obsidian or /Users/you/Obsidian)
What is your meta vault path? (e.g. ~/Obsidian/meta)
```

Confirm: check both paths exist before proceeding.

## Step 3 — Collect vault list

List all immediate subdirectories of `obsidian_root` that contain a `CLAUDE.md` file.
Exclude: `inbox/`, `planning/`, `meta/`, and hidden directories.

Present the list and ask:
- Which vaults participate in the inbox pipeline? (`inbox: true`)
- Which are discovery-only (wiki-sync reads them but inbox does not route to them)?

## Step 4 — Collect inbox routing rules

Present the current routing table (if updating) or a starter template (if new).

For each routing entry, confirm:
- `intent` tag
- `signals` — content patterns that identify this intent
- `target_vault` — vault id from the vault list
- `target_subpath` — path within that vault, using `{ts}` for timestamp

Flag any vaults referenced in routing that are not in the vault list.

## Step 5 — Write config

Show the complete proposed `wiki-manager.config.yaml`. Ask: "Write this? (yes / edit)"

On yes: write to `{OBSIDIAN_META}/wiki-manager.config.yaml`.

Report: `wiki-manager-config: written to {OBSIDIAN_META}/wiki-manager.config.yaml`

See `references/config-schema.md` for the full field reference.
