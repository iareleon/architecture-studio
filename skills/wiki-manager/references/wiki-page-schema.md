# Wiki Page Schema

## Frontmatter

```yaml
---
title: {Page Title}
status: 🟡 harvesting | 🟠 drafting | 🟢 approved | 🚀 in sprint
last_updated: YYYY-MM-DD
sprint: {sprint-id or null}
---
```

## Status meanings

| Status | Meaning | Who sets it |
|--------|---------|-------------|
| 🟡 harvesting | Raw content, open questions, brain dump in progress | Agent after session |
| 🟠 drafting | Main gaps filled, being refined and cross-referenced | Agent after distill |
| 🟢 approved | User has reviewed and confirmed — ready for sprint | User only |
| 🚀 in sprint | Being executed against | Agent after sprint card created |

Never skip a stage. Never mark 🟢 without explicit user confirmation.

## Required sections per page type

### Vision page
- Problem statement
- What this platform does
- What it is NOT
- Target buyer
- Success criteria (6 months post-deploy)
- Open questions

### Architecture page
- Repo list
- Layer boundaries diagram
- Key constraints
- Open questions

### Knowledge-model page
- Graph nodes
- Graph edges
- Second-brain layer structure
- Knowledge writer contract
- Open questions

### Compliance-model page
- Domains in scope
- Scoring model
- Rubric storage
- Evidence model
- Open questions

### Integration page
- Protocol
- Connectors (one section per integration)
- Ingestion pipeline
- Open questions
