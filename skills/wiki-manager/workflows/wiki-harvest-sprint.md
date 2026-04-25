# Wiki Harvest — Sprint

Converts an approved wiki page into a self-contained sprint card.

If a persona is loaded, apply its sprint constraints, repo naming, and ADR rules to the card.

## Precondition

Page must be 🟢 approved. Refuse if status is 🟡 or 🟠.

## 1. Read the page

Read the approved wiki page in full.

If a persona is loaded: also read the files specified in the persona's path guidance (ADR index, sprint index, skills registry).

## 2. Determine sprint number

Read the sprint index file (path from persona, or ask user if not set). Use next available sprint number.

## 3. Draft the sprint card

```markdown
# Sprint {N} — {scope}

## Goal
{one sentence}

## Repo
{repo name — from persona or ask user}

## Scope
Files to create:
- ...
Files to modify:
- ...

## Acceptance criteria
- [ ] ...
- [ ] ...

## Constraints
{from persona ADRs and non-negotiables, or leave blank if no persona loaded}

## Skills to activate
- {relevant skills}

## Execution plan
1. ...
2. ...

## Definition of done
- [ ] PR raised with all acceptance criteria met
- [ ] Run log written
- [ ] CLAUDE.md updated if architecture decisions changed
```

## 4. Confirm before writing

Show the draft sprint card. Ask:
```
Does this sprint card capture the right scope? (yes / edit / cancel)
```

On yes: write to the sprint folder (path from persona, or ask user). Update sprint index — add the new sprint, mark source page as 🚀 in sprint.

On cancel: discard, leave page status unchanged.

## 5. Task management

If `project-manager` skill is active: load it and create the corresponding task card.
If not active: remind user to create the task manually.
