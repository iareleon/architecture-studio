# Knowledge OS pack (SkillsLoom repo)

During **UAT**, run Knowledge OS procedures from a terminal (e.g. Claude CLI) using the **`wiki-manager`** skill under `skills/wiki-manager/`; broader scheduling or automation is deferred until after UAT.

**Knowledge OS** is an Obsidian-based personal knowledge system built around a `meta` master vault. It provides an inbox for unclassified capture, domain vaults for organised knowledge, and CLI-driven index refresh run manually in a terminal. SkillsLoom integrates with it via the **`wiki-manager`** skill and terminal-first workflow prompts.

This folder ships the integration layer — environment config, terminal workflow prompts, and vertical pilots — but does **not** include the Knowledge OS operation skills (`classify`, `core/`) themselves; those live in a separate install (e.g. choreokit). See [docs/knowledge-os.md](../docs/knowledge-os.md) for the full architecture.

## Contents

- [knowledge-os.env.example](knowledge-os.env.example) — environment variable template (`OBSIDIAN_ROOT`, `OBSIDIAN_META`, `SKILLSLOOM_DIR`)
- Terminal workflow prompts — manual Claude CLI runs for Knowledge OS operations
- [pilot/estate/](pilot/estate/) — estate agency pilot: vault skeleton, runbook, and CLI cadence

**Documentation:** [docs/knowledge-os.md](../docs/knowledge-os.md)

**CLI:** `skillmanager knowledge-os` — verifies `OBSIDIAN_META` layout and SkillsLoom symlinks for key Knowledge OS skills
