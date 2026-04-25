---
name: <skill-name> (use only in real SKILL.md; optional frontmatter for docs)
description: <One-line summary of what this workflow does and the outcome it produces>. Invoke when <specific user intent or trigger scenario>.
metadata:
  version: "1.0"
  disable-model-invocation: true
---

# <Workflow Title>

<Brief paragraph: what this workflow automates, why it exists, what problem it solves.>

## Workflow

### 1. <Gather / Inspect>
<What information to collect or inspect before acting.>

### 2. <Process / Draft>
<What to compute, generate, or prepare.>

### 3. Confirm with User

Present the result for approval before taking any irreversible action.
Do not proceed without explicit confirmation.

```
<structured preview format — adapt to the workflow's output>

Proceed? (yes / edit / cancel)
```

### 4. Execute

Upon approval:
- <Action 1>
- <Action 2>
- Confirm success with a status check.

## Guidelines

- **Never act silently:** Always present a summary and wait for approval before irreversible actions.
- **Respect scope:** Only act on what the user explicitly requested.
- <Additional constraint specific to this workflow>

## Subflows

<!-- Optional. Only include if this skill routes to more files in workflows/.
     Remove this section if not needed.

| File | Load when |
|---|---|
| `workflows/<workflow-name>.md` | <condition that triggers this file> |

-->

## References

<!-- Optional. List files to read lazily — only when a step explicitly needs them.
     Store lookup tables, config schemas, or large reference docs in references/<name>.md.
     Remove this section if no reference files are needed.

- `references/<name>.md` — <what it contains>; read during Step <N>

-->
