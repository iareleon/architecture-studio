---
name: vault-paths
description: Knowledge base path resolution — locate files across multiple workspaces or vaults, read cross-workspace rules, and confirm allowed writes before touching more than one location. Invoke when routing paths or following cross-workspace links.
metadata:
  version: "1.1"
  disable-model-invocation: true
---
# Vault paths

**Intent:** this skill is only for **resolving where things live** and **which workspace's rules apply** — not for drafting content, tasks, or classification logic (use `wiki-harvest`, `project-manager`, or your inbox automation for those).

> **Tool note:** bundled references use an Obsidian multi-vault layout as the default example. For other knowledge base systems (Notion, Confluence, local folders, etc.) update `references/vault-map.md` with your workspace paths and rules. All principles below are tool-agnostic.

**Main brain:** this file. `references/vault-map.md` is the canonical list of install-specific paths. Do not use `memory/baseline.md` for this skill.

## Before any multi-workspace operation

1. Read `references/vault-map.md`
2. Read the target workspace's `cross-vault-links.md` (or equivalent boundary rules file) if it exists
3. Confirm the operation is allowed for that workspace

## Routing (indicative — your `vault-map` wins)

| Need | Often under |
|------|-------------|
| Platform / architecture content | Architecture workspace |
| Personal / reflective notes | Personal workspace |
| Social / long-form content | Content workspace |
| Strategy / company content | Company workspace |
| Delivery / project tracking | Project workspace |
| Skills install | `~/.skillmanager/skills/` or Skill Forge clone |

(Replace with your actual paths in `references/vault-map.md`.)

## Write rules (summary)

- Never write without reading that workspace's rules. Personal layer: soul subflows only; never sanitise. Content workspaces: confirm before writing. Boundary rules file is authoritative.
- If a file is "missing," check boundary rules and aliases before assuming it does not exist.
- Respect Filesystem / MCP allowlists for the workspace.

## References

- `references/vault-map.md`
