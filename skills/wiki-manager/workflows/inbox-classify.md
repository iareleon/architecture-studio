# Inbox Classify

Classifies files in the meta inbox raw folder and stages them to review.

## Step 0 — Load config

Read `{OBSIDIAN_META}/wiki-manager.config.yaml`.

Extract:
- `inbox.raw` → full path: `{obsidian_meta}/{inbox.raw}`
- `inbox.review` → full path: `{obsidian_meta}/{inbox.review}`
- `routing` → classification rules table

## Step 1 — Scan raw inbox

List all `.md` files in `{obsidian_meta}/{inbox.raw}` at depth 1.

If empty: report "inbox/raw is empty — nothing to classify." and stop.

## Step 2 — Classify each file

For each `.md` file that does not already have an `intent:` frontmatter field:

**2a — Determine intent**

Apply in priority order:
1. Existing `intent:` frontmatter → skip, file is already classified
2. First-line prefix (e.g. `#soul`, `#bible`, `#product`) → use directly as intent
3. Body content → match against `signals` in the routing table

**2b — Write frontmatter**

Prepend or merge a YAML frontmatter block using flat bare keys:

```yaml
---
intent: <intent>
confidence: <0.0–1.0>
target_vault: <vault id from config>
target_subpath: <path pattern with {ts}>
sub_intent: <sub_intent or omit>
classified_at: <YYYY-MM-DD>
reasoning: <one-line explanation>
---
```

Rules:
- Never modify original content below the frontmatter.
- For `ambiguous` intent: set `confidence` below 0.5, set `target_vault: ""`, flag clearly in `reasoning`.
- For folder bundles (multiple files): classify by dominant theme. If files span multiple vaults, set `intent: ambiguous`.
- `{ts}` format: `YYYYMMDD-HHMMSS`

**2c — Move to review**

Move the updated file to `{obsidian_meta}/{inbox.review}`.

Report per file: `<filename> → <intent> (<confidence × 100>% confidence) → staged to review/`

## Step 3 — Report

```
inbox-classify: {obsidian_meta}/inbox/
  Files scanned: {N}
  Classified: {N}
  Ambiguous (flagged): {N}
  Already classified (skipped): {N}
  → staged to review/
```
