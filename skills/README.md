# Skills

All skills live in a **flat** tree: `skills/<name>/` with a single `SKILL.md` (usually a **router** — a short load map; details live in `workflows/`, `memory/`, `references/`, and optional `templates/` / `scripts/`). See [Domain layout](../docs/domain-layout.md).

There is **no** `-sme` or `-wf` suffix. One folder = one activatable skill.

Every skill is only `skills/<name>/`. Set **`metadata.status`** in `SKILL.md` to `active` (default), `staging`, `review`, `deactivated`, or `decommissioned`, then run **`skillmanager audit`** so symlinks in `~/.claude/skills` (and staging dirs when needed) match.

`skillmanager` symlinks every **active** skill into your LLM skills directory so the whole tree (including `workflows/` and `memory/`) is readable when invoked.

**Intent:** a skill should **augment** a human (clear procedures, SME context, drafts you approve). **Canonical knowledge** and routing live in your wikis—e.g. Obsidian `meta` (inbox, `_os/`, `wiki/`) and domain vaults—driven manually via **`wiki-manager`** workflows in a terminal until any post-UAT automation is explicitly scoped.

## Create a new skill

Use the `skill-manager` skill, or copy a template from `skill-manager/templates/`:

```bash
cp skills/skill-manager/templates/expertise-skill-template.md skills/<your-skill>/SKILL.md
# or workflow-style template
cp skills/skill-manager/templates/workflow-skill-template.md skills/<other-skill>/SKILL.md
```

Edit placeholders and frontmatter per `docs/skill-spec.md`. The `name:` field must match the directory name exactly (e.g. `name: my-api` ↔ `skills/my-api/`).

## Naming

- Lowercase, hyphen-separated; start with a letter
- **Not** a reserved path name: `review`, `deactivated`, `staging`, `decommissioned`, `sme`, `workflow`
- Optional: `-sys` suffix for rare system/validator skills

Run `python3 scripts/check_skill_names.py` and `skillmanager audit` to validate.

## Upgrading from `-sme` / `-wf`

Rename `skills/foo-sme` → `skills/foo` (merge with `foo-wf` if you had both), set `name:` in `SKILL.md` (main brain for that skill), add optional `persona/` or `references/` as needed, then re-run `skillmanager audit`. Per-skill `memory/baseline.md` is legacy—prefer `SKILL.md` + project `CLAUDE.md`.
