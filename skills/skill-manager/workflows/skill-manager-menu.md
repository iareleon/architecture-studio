# Skill Manager — Menu & CLI Reference

Authors new skills, monitors sessions for skill gaps, and audits content quality.
State is managed by the `skillmanager` CLI — never by this skill directly.

## CLI Delegation

For symlink and health operations, emit the appropriate command and stop:

| Intent | Command |
|---|---|
| List all skills (status + symlinks) | `skillmanager ls` |
| Align symlinks to `metadata.status` in each `SKILL.md` | `skillmanager audit` (alias: `skillmanager sync`) |
| Check status ↔ symlinks | `skillmanager status` |
| Environment check | `skillmanager doctor` |

To hide or stage a skill, edit `metadata.status` in `skills/<name>/SKILL.md`, then run `skillmanager audit`.

## Subflows

Load the relevant subflow only when the user's intent matches:

| File | Load when |
|---|---|
| `workflows/skills-create.md` | User wants to create or scaffold a new skill |
| `workflows/skills-detect.md` | Monitoring session for skill gaps (background protocol) |
| `workflows/skills-audit.md` | Auditing skill content, frontmatter, or memory references |
| `workflows/skills-propose.md` | User wants to propose a new skill to the Skill Manager repository |
| `workflows/skills-refine.md` | User wants to improve an existing skill's content |

## Guidelines

- Always write new skills to `${SKILLMANAGER_DIR}/skills/` — never to the working directory.
- To retire a skill from the LLM, set `metadata.status: decommissioned` and run `skillmanager audit` (files stay on disk).
- After authoring a skill, always end with: `Run: skillmanager audit`
- Keep `SKILL.md` lean — move content >10 lines into `references/` or subflow files.
- Memory scaffolding (stub creation, list, archive) is owned by `memory`.
- **Authoring templates**: `templates/expertise-skill-template.md` and `templates/workflow-skill-template.md`; one primary capability per skill.
- **Quality bar**: run `skillmanager audit` after substantive edits; for checklist-style audits, load the relevant file under `references/auditor-personas/`.

## References

- `references/marketplace-overlap.md` — plugin conflict data; check when creating skills that overlap with Claude plugins
- `references/mcp-playbook.md` — MCP server setup (generic); see `references/mcp-playbook-claude.md` for Claude-specific config
- `references/auditor-personas/structural.md` — workspace structure and naming audits
- `references/auditor-personas/compliance.md` — skill formatting and policy audits
- `references/auditor-personas/performance.md` — context and efficiency audits
- `references/auditor-personas/prompt.md` — prompt redundancy and pattern audits
- `references/auditor-personas/audit-report.template.md` — audit report scaffold
