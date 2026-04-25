# Inbox Dispatch

Moves approved files from the meta inbox to their target vault inboxes.

## Step 0 — Load config

Read `{OBSIDIAN_META}/wiki-manager.config.yaml`.

Extract:
- `inbox.approved` → full path: `{obsidian_meta}/{inbox.approved}`
- `vaults` → map of vault id → path

## Step 1 — Scan approved inbox

List all `.md` files in `{obsidian_meta}/{inbox.approved}` at depth 1.

If empty: report "inbox/approved is empty — nothing to dispatch." and stop.

## Step 2 — Dispatch each file

For each `.md` file found:

**2a — Read routing fields**

Read the file's frontmatter. Required fields:
- `intent`
- `target_vault`
- `target_subpath` (contains `{ts}` placeholder)

If any required field is missing or `target_vault` is empty (ambiguous): skip the file, flag it for manual review.

**2b — Resolve destination**

Look up `target_vault` in the config vaults list to get the vault root path.

Resolve `{ts}` in `target_subpath` to the current timestamp (`YYYYMMDD-HHMMSS`).

Full destination: `{vault_path}/{target_subpath}`

**2c — Move file**

Create parent directories if they do not exist.

Move the file to the resolved destination path.

Report: `<filename> → {vault_id}/inbox/raw/ → <destination filename>`

## Step 3 — Report

```
inbox-dispatch: {obsidian_meta}/inbox/approved/
  Files dispatched: {N}
  Skipped (ambiguous / missing fields): {N}
  → moved to vault inbox/raw/ folders
```
