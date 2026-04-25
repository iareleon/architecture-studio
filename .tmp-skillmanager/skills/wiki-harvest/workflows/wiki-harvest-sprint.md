# Wiki Harvest — Sprint Subflow

Converts an approved wiki page into a self-contained sprint card for Claude Code.

## Precondition

Page must be 🟢 approved. Refuse if status is 🟡 or 🟠.

## 1. Read the page

Read the approved wiki page in full.
Read `decisions/ADR-index.md` for relevant constraints.
Read `context/skills-registry.md` for available skills.

## 2. Determine sprint number

Read `sprints/sprint-index.md`. Use next available sprint number.

## 3. Draft the sprint card

```markdown
# Sprint {N} — {scope}

## Goal
{one sentence}

## Repo
product-meridian-{component}

## Scope
Files to create:
- ...
Files to modify:
- ...

## Acceptance criteria
- [ ] ...
- [ ] ...

## Constraints
- Hexagonal architecture — domain layer has no infrastructure imports
- No GCP-specific dependencies in core
- All tests passing before PR
- CLAUDE.md exists at repo root

## Skills to activate
- architect
- development-engineer
- {others as relevant}

## Execution plan
1. ...
2. ...
3. ...

## Definition of done
- [ ] PR raised with all acceptance criteria met
- [ ] Claude Code run log written to Runs/
- [ ] CLAUDE.md updated if architecture decisions changed
```

## 4. Confirm before writing

Show the draft sprint card. Ask:
```
Does this sprint card capture the right scope? (yes / edit / cancel)
```

On yes: write to `sprints/sprint-{NN}-{slug}.md`.
Update `sprints/sprint-index.md` — add the new sprint, mark source page as 🚀 in sprint.

## 5. Create ClickUp task

If `project-manager` is active: load it → `workflows/project-manager-create.md` → sprint card format.
If not active: remind user to create the ClickUp task manually.
