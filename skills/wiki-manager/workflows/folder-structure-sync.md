# Folder Structure Sync

Generates or updates `_structure.md` in a target folder with a Mermaid diagram of current contents. Call after any file create, rename, move, or delete within a vault folder.

## Input

`folder-path` — absolute path to the folder to document (e.g. `~/Obsidian/bible-study/wiki/` or `{vault}/wiki/`).

## Step 1 — List folder contents

List all files and immediate subdirectories in `folder-path`.

Exclude:
- `_structure.md` itself
- Hidden files and directories (names starting with `.`)
- Files matching `*.routing`

Sort: directories first (alphabetically), then files (alphabetically).

## Step 2 — Build the Mermaid graph

Construct a `graph TD` Mermaid diagram.

Rules:
- Root node ID: `ROOT` with label `["{folder-name}/"]`
- Each immediate subdirectory: `D_{slug}("{dirname}/ ({N} items)")`
- Each immediate file: `F_{slug}["{filename}"]`
- Connect all nodes to `ROOT` with `-->`

Node ID slugs: replace non-alphanumeric characters with `_`, prefix with type (`D_` or `F_`).

## Step 3 — Write `_structure.md`

```markdown
# Folder: {folder-name}/
Last updated: {YYYY-MM-DD}
Skill: wiki-manager

\`\`\`mermaid
graph TD
  ROOT["{folder-name}/"]
  ...
\`\`\`

| Name | Type | Items |
|---|---|---|
| {name} | dir/file | {count or —} |
```

## Step 4 — Report

```
folder-structure-sync: {folder-path}
  Nodes: {N files + M dirs} → _structure.md updated
```

## Rules

1. Never recurse into subdirectories — document one level only.
2. Never modify any file other than `_structure.md` in the target folder.
3. If `_structure.md` already exists, overwrite it entirely.
4. If the folder is empty: write `ROOT["{folder-name}/"] --> EMPTY["(empty)"]`
5. Model tier is haiku — list structure only, no content analysis.
