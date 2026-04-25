# Skills Create Subflow

Guides the user through authoring a new skill — collecting name, type, structure, and
content — then writes all files **only after explicit user approval**.
Activation is always delegated to the `skillmanager` CLI.

> **Global rule:** Do not write any file until the user has reviewed and approved the full
> preview. If confidence in any detail is < 95%, surface the uncertainty and ask before
> proceeding. Human sign-off is required at every gate.

## Naming standard

Skill directory = **one kebab-case name** (e.g. `git`, `devops`, `my-api`). No `-sme` / `-wf` suffix.

## Workflow

### 1. Collect name and type

```
What type of skill?

  1. sme-persona  — domain expertise and standards (e.g. architect, security)
  2. workflow     — step-by-step procedures (e.g. git, terraform)

Enter 1 or 2:
```

Then:

```
Skill name (lowercase, hyphen-separated, final directory name):
```

Show the resolved name and confirm:

```
Skill will be created as: skills/<name>/
Continue? (yes / cancel)
```

Validate: `^[a-z][a-z0-9-]+$`, not a reserved name (`review`, `deactivated`, `staging`, `decommissioned`, `sme`, `workflow`). Run `skillmanager ls` to avoid duplicates.

### 2. Determine Subflow File Structure

For `sme-persona`: skip — these skills are single-file by nature.

For `workflow`: ask:

```
Will this skill have multiple distinct operations?
If yes, list each operation name (one per line). These become subflow files under workflows/.
If no, all workflow steps stay in SKILL.md.

Examples: "create", "detect", "audit" → skills-create.md, skills-detect.md, skills-audit.md
```

Collect the list of subflow names (or none).

### 3. Collect Description

```
One-line description (what it does and when to invoke it):
```

### 4. Collect Body Content

**sme-persona**: Collect in order — Focus area, Standards (bullet list),
Mandatory tasks (numbered list), Constraints (bullet list).

**workflow SKILL.md** (with subflows): Collect only the routing logic —
what each subflow does and when to load it.

**workflow SKILL.md** (single file): Collect full workflow steps — problem
statement, step names, guidelines.

**For each subflow file**: Collect separately — step names and descriptions, guidelines.

### 5. Collect Reference Files

```
Does this skill need reference files (lookup tables, specs, lists >10 lines)?
If yes, describe each one. (yes / no)
```

If yes: collect name and content for each. Write to `references/<name>.md` inside
the skill directory. Add a `## References` section listing each file and the
step/condition that triggers loading it.

### 6. Preview and Confirm

Display the generated `SKILL.md` and any subflow files. Ask:

```
Does this look correct? (yes / edit / cancel)
```

On `edit`: ask which section to change, collect the replacement, re-display.
On `cancel`: stop — nothing is written.

### 7. Write Files

All files are written to `${SKILLMANAGER_DIR}/skills/` — never to the working directory.

Target: `${SKILLMANAGER_DIR}/skills/<name>/` (one folder per skill).

1. Create the skill directory
2. Write `SKILL.md` using the appropriate template:
   - `sme-persona` → `templates/expertise-skill-template.md`
   - `workflow` → `templates/workflow-skill-template.md`
3. Write each subflow file under `workflows/` using `templates/workflow-file-template.md`
4. Write each `references/<file>.md` if collected in Step 5
5. Check `references/marketplace-overlap.md` — warn on any conflict
6. Confirm:
   ```
   Created: ${SKILLMANAGER_DIR}/skills/<type>/<name>/
   Files:   SKILL.md<, subflow files, reference files>
   ```

### 8. Delegate Activation

```
Run: skillmanager audit
```

Do not create symlinks inline — the CLI owns that operation.
Offer to create a memory stub: ask the user to invoke `brain-manager` for that.

## Guidelines

- Never write skill files outside `${SKILLMANAGER_DIR}/skills/`.
- A skill with a single operation keeps everything in `SKILL.md` — do not split prematurely.
- Reference rule: any content >10 lines needed for only one step belongs in `references/`, not inline.
- Subflow files have no frontmatter — they are markdown documents loaded lazily by the parent SKILL.md.
