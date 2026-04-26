---
name: project-manager
description: "Create, update, and query work in the configured task tool; route blockers, sprint items, and proposals to the right list. Use when the user says track this, add a card, what is blocked, move it to the sprint, or file a follow-up for the team — even if they never name Linear/Jira/Asana and only describe a next step."
metadata:
  version: "1.1"
  disable-model-invocation: true
---
# Project manager (task management)

**Main brain:** this file. Tool-specific IDs and list references — **never** hardcode IDs in prose without reading the IDs file first.

**ID lookup order (stop at first file that exists):**
1. `references/task-tool-ids.local.md` — your real workspace IDs (gitignored, never committed)
2. `references/task-tool-ids.md` — framework template with placeholder values

> **Tool note:** bundled references default to **ClickUp**. For other tools (Linear, Jira, Asana, GitHub Issues, etc.) replace `references/task-tool-ids.md` and update the connector in `workflows/` to match your tool's API or MCP. All workflow patterns below are tool-agnostic.

Your configured task management tool is the source of truth for tracked project work when this skill is active. Operations via the configured MCP connector or CLI.

## Subflows

| File | When |
|------|------|
| `workflows/project-manager-create.md` | New task, blocker, proposal |
| `workflows/project-manager-query.md` | Status, open items (add this file if missing) |
| `workflows/project-manager-update.md` | Comments, status, close (add this file if missing) |
| `workflows/project-manager-sprint.md` | Sprint cards (add this file if missing) |

## Routing (illustrative — confirm IDs in `references/task-tool-ids.md`)

| Intent | Pattern | Target (verify in references) |
|--------|---------|--------------------------------|
| Agent blocker | create | Platform improvements list |
| Skill proposal | create | Features backlog + tag `agent-proposal` |
| Sprint | sprint | Active sprint board |
| Status | query | Relevant list or board |

## Guidelines

- Read `references/task-tool-ids.md` before any write — never assume IDs. Apply rate limiting and backoff per your tool's API limits. Failed writes must be queued — never dropped silently. Tag agent-created tasks `agent-created`, proposals `agent-proposal`, blockers `blocker`.

## References

- `references/task-tool-ids.local.md` — your real workspace IDs (gitignored; create this file and fill it in)
- `references/task-tool-ids.md` — framework template; shows the expected structure
