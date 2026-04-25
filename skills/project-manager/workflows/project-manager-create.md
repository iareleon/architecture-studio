# ClickUp Create Subflow

Creates a new task in the correct ClickUp list based on intent.

## 1. Determine intent

| Intent | List | Required fields |
|--------|------|----------------|
| Agent blocker | Platform improvements | title, description, priority: urgent |
| Skill proposal | Forgemaster features | title, description, subtype, tag: agent-proposal |
| Sprint card | Meridian product list | title, description, phase, acceptance criteria |
| Pattern / learning | Forgemaster features | title, description, subtype: Observed Pattern |
| General task | Confirm with user | title, description, priority |

## 2. Build the task

**Agent blocker format:**
```
Title: [FM-BLOCKER] {product} — {short description}
Description:
  What was attempted: ...
  What failed: ...
  Options for Leon: ...
  Resume with: exact instruction to continue
Priority: Urgent
Tags: agent-created, blocker
```

**Skill proposal format:**
```
Title: [SKILL PROPOSAL] {skill-name} — {one-line description}
Description:
  Observed in: {session / product / task}
  What it would do: ...
  Why it has broader applicability: ...
  Suggested type: sme-persona | workflow
Subtype: Observed Pattern / Session Learning
Tags: agent-created, agent-proposal
```

**Sprint card format:**
```
Title: Sprint {N} — {scope description}
Description:
  Goal: one sentence
  Scope: files to create/modify
  Acceptance criteria: bulleted list
  Constraints: from CLAUDE.md
  Execution plan: numbered steps
Tags: agent-created, sprint
```

## 3. Confirm before writing

Show the full task to the user before creating:
```
Creating task in {list}:
  Title: ...
  Description: ...
  Tags: ...
Confirm? (yes / no)
```

On agent-created blockers during autonomous build: skip confirmation — write immediately.

## 4. Write

Use ClickUp MCP to create the task.
On failure: append to `.forgemaster/ClickUp Write Queue.json`.
Confirm: `Task created: {task-id} — {title}`
