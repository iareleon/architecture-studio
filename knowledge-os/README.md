# Knowledge OS pack (Skillforge repo)

**Knowledge OS** is an Obsidian-based personal knowledge system built around a `meta` master vault. It provides an inbox for unclassified capture, domain vaults for organised knowledge, and automated index refresh via scheduled AI tasks. Skillforge integrates with it by supplying the `wiki-harvest` and `vault-paths` skills and a set of ready-to-paste Cowork task templates.

This folder ships the integration layer — environment config, Cowork task templates, and vertical pilots — but does **not** include the Knowledge OS op-skills (`classify`, `core/`) themselves; those live in a separate install (e.g. choreokit). See [docs/knowledge-os.md](../docs/knowledge-os.md) for the full architecture.

## Contents

- [knowledge-os.env.example](knowledge-os.env.example) — environment variable template (`OBSIDIAN_ROOT`, `OBSIDIAN_META`, `SKILLMANAGER_DIR`)
- [cowork/](cowork/) — Claude Cowork scheduled task instructions (versioned, paste-ready)
- [pilot/estate/](pilot/estate/) — estate agency pilot: vault skeleton, memory template, and Cowork schedule

**Documentation:** [docs/knowledge-os.md](../docs/knowledge-os.md)

**CLI:** `skillmanager knowledge-os` — verifies `OBSIDIAN_META` layout and Skillforge symlinks for key Knowledge OS skills
