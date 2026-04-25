# Vault Inbox Sync

Processes approved files from all vault inboxes, moves them to their final destinations within the vault, and triggers a wiki sync for any vault with changes.

## Step 0 — Load config

Read `{OBSIDIAN_META}/wiki-manager.config.yaml`.

Extract:
- `vaults` — list of all vaults with `inbox: true`
- `obsidian_meta` — for the final wiki-sync step

## Step 1 — Scan vault inboxes

For each vault with `inbox: true`:

Check `{vault_path}/inbox/approved/` for `.md` files.

Build a list of (vault, file) pairs with pending approved items. If all vaults are empty: report "All vault inboxes are empty — nothing to process." and stop.

## Step 2 — Process each vault

For each vault that has approved items:

**2a — Read file frontmatter**

For each `.md` file in `{vault_path}/inbox/approved/`:

Read `target_subpath` from frontmatter. This is the final destination within the vault (e.g. `raw/YYYYMMDD-HHMMSS-intent.md`).

If `target_subpath` is missing: use `raw/{original-filename}` as fallback and flag.

**2b — Move to final destination**

Full destination: `{vault_path}/{target_subpath}`

Create parent directories if needed. Move the file.

Report per file: `<filename> → {vault_id}/{target_subpath}`

**2c — Mark vault as changed**

Add vault to the changed-vaults list for Step 3.

## Step 3 — Chain to wiki-sync

For each vault in the changed-vaults list: follow `wiki-sync.md` for that vault only (changed-vault mode — skip unchanged vaults using their existing `_super-wiki.md` rows).

See `wiki-sync.md` for the full vault discovery and log-diff protocol.

## Step 4 — Report

```
vault-inbox-sync:
  Vaults scanned: {N}  (with items: {N})
  Files processed: {N}
  Skipped (missing target): {N}
  → wiki-sync run for {N} changed vaults
```
