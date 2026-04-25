# Task Tool IDs — Framework Template

> **This is the committed template.** Do NOT fill in real IDs here.
>
> **To configure your workspace:** copy this file to `task-tool-ids.local.md` in the same directory and fill in real values there. That file is gitignored and will never be committed.
>
> ```bash
> cp skills/project-manager/references/task-tool-ids.md \
>    skills/project-manager/references/task-tool-ids.local.md
> ```
>
> For ClickUp: source IDs from your ClickUp workspace settings (Settings → Workspace, then navigate to each Space/Folder/List and copy the ID from the URL).
> For other tools: adapt the structure to match your tool's ID hierarchy (org, project, board, list, etc.).

**Last updated:** YYYY-MM-DD
**Tool:** ClickUp | Linear | Jira | Asana | GitHub Issues | (your tool here)

## Workspace / Organisation

| Key | Value |
|-----|-------|
| Workspace / Org ID | `<your-workspace-id>` |
| Primary space / project | `<your-space-id>` |
| Primary folder / group | `<your-folder-id>` |

## Lists / Boards

| List | ID |
|------|----|
| Platform improvements | `<id>` |
| Feature backlog | `<id>` |
| Bug backlog | `<id>` |
| (add your lists here) | `<id>` |

## Standard tags

| Tag | Use |
|-----|-----|
| `agent-created` | All tasks created by an agent |
| `agent-proposal` | Observed patterns / learning proposals |
| `blocker` | Tasks blocking agent progress |
| `agent-blocked` | Tasks where agent was blocked mid-build |
