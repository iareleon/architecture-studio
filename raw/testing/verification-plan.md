---
name: Skill Forge Verification Plan
description: A gated, step-by-step manual verification guide. Canonical copy for multi-session work — update the progress table as you go.
todos:
  - id: phase-0
    content: "Phase 0: Run skillmanager doctor, config, version, ls, status — confirm environment is healthy"
    status: completed
  - id: phase-1
    content: "Phase 1: Verify LLM skill symlinks exist and memory skill is visible in Cursor/Claude"
    status: completed
  - id: phase-2
    content: "Phase 2: Test memory write, scope confirmation, and archive flows with diff + approval"
    status: completed
  - id: phase-3
    content: "Phase 3: Test memory-audit, memory-create, and memory-system-toggle workflows"
    status: completed
  - id: phase-4
    content: "Phase 4: Test per-skill persona memory routing (development-engineer/persona/python.md)"
    status: completed
  - id: phase-5
    content: "Phase 5: Run skill-manager audit and review-one on the memory skill"
    status: completed
  - id: phase-6
    content: "Phase 6: Verify Knowledge OS Cowork tasks (inbox-process, super-wiki-refresh, wiki-harvest)"
    status: pending
---

# Skill Forge Verification Plan

A phased, gated guide. Each phase ends with a confirmation gate — only proceed when you are satisfied. Signal readiness with: **"Phase N done — move on"** or flag any issues for triage before continuing.

---

## How to use this file

**This is the canonical copy** in the repo (`raw/testing/verification-plan.md`). At the start of a new session, use the **Session resume prompt** below. Keep the **Progress tracker** table in sync with reality (edit this file, then commit).

---

## Session resume prompt

Copy and paste this at the start of any new chat session:

```
Read raw/testing/verification-plan.md. We are working through the Skill Forge
verification plan. Check the progress table and tell me which phase we are on,
what was last completed, and what the next step is. Wait for my confirmation
before doing anything.
```

---

## Progress tracker

Update this table as each phase is completed. Mark the status column and add a one-line outcome note.

| Phase | Title | Status | Outcome / Notes |
|-------|-------|--------|-----------------|
| 0 | Environment Health Check | `done` | Fixed install_dir (old path → ~/.skillmanager), re-ran install.py, all 16 skills OK |
| 1 | Skill Symlinks and Visibility | `done` | Skills visible in Cursor agent; symlinks match after ~/.skillmanager install |
| 2 | Memory Skill: Basic Write + Approval Flow | `done` | 2a: no-op on existing fact; 2b: global scope confirmed, wrote to install_dir/model.md; 2c: archive comment used, restored after |
| 3 | Memory Skill: Audit + Create + Toggle | `done` | 3a: audit read-only, no issues found, I-6 raised for last-updated; 3b: python-preferences.md stub created with approval, router entry added to SKILL.md; 3c: toggle explained both modes, no system-skills block in model.md — flag for installer |
| 4 | Memory Routing: Per-Skill Persona Files | `done` | 4a: read python.md correctly; 4b: update routed to persona file, showed diff, required approval, wrote on "yes" |
| 5 | Skill Manager: Skill Health | `done` | 5a: 9 skills gained ## References sections; 4 persona files got last-updated; scripts/skills_audit.py added; all 16 pass clean. 5b: memory skill keep — near-pass; added 2 missing librarian templates to References |
| 6 | Knowledge OS Cowork Automations | `pending` | |

Status values: `pending` → `in-progress` → `done` or `blocked: <reason>`

---

## Phase 0 — Environment Health Check

**Goal:** Confirm the Skill Forge install is intact before testing anything else.

Run each command and check the expected output:

```bash
skillmanager doctor        # should report all tools found, no PATH errors
skillmanager config        # should show SKILLMANAGER_DIR, LLM targets (claude etc.)
skillmanager version       # should print a version string
skillmanager ls            # should list all 16 skills with their metadata.status
skillmanager status        # should confirm symlinks match metadata.status
```

What to watch for:
- `doctor` flags missing tools (git, gh, gcloud, terraform) — note any gaps
- `config` confirms `~/.skillmanager/config.yaml` exists and `install_dir` is a real path (e.g. `~/.skillmanager`)
- `ls` shows all skills; any unexpected `deactivated` or missing entries
- `status` shows no mismatched symlinks (if it does, run `skillmanager audit` to fix)

Key files checked implicitly:
- [`scripts/skillmanager.py`](../../scripts/skillmanager.py) — the CLI
- `~/.skillmanager/config.yaml` — install config

> **Gate 0:** Confirm `doctor` is clean and all 16 skills are visible in `ls`. Flag any red flags before proceeding.

**Phase 0 notes** _(fill in during testing)_:
- [ ] `doctor` clean
- [ ] `config` shows correct `install_dir`
- [ ] `ls` shows 16 skills
- [ ] `status` shows no mismatched symlinks
- Findings:

---

## Phase 1 — Skill Symlinks and Visibility

**Goal:** Confirm LLM clients (Cursor, Claude Code, Cowork) can see the skills.

Steps:
1. Locate your LLM skills dir: `skillmanager config` will show the path (typically `~/.claude/skills/`)
2. List the symlinks there: `ls -la ~/.claude/skills/`
3. Verify at least the key skills are symlinked: `memory`, `skill-manager`, `vault-paths`, `documenter`, `git`
4. If any are missing, run `skillmanager audit` to reconcile

In Cursor, attach skills from the skills picker. In Claude Code, skills load per product behavior.

> **Gate 1:** Confirm skills are visible. Confirm `memory` skill is reachable when you need it.

**Phase 1 notes** _(fill in during testing)_:
- [ ] `~/.claude/skills/` contains correct symlinks
- [ ] `memory` skill symlink exists and is not broken
- [ ] Skills visible/attachable in Cursor (or your primary client)
- Findings:

---

## Phase 2 — Memory Skill: Basic Write + Approval Flow

**Goal:** Verify the end-to-end memory write cycle works correctly with diff + approval.

The [`../../skills/brain-manager/SKILL.md`](../../skills/brain-manager/SKILL.md) core workflow:
1. Detect trigger phrase → identify target file → show diff → write only on "yes"

**Test 2a — Project memory (CLAUDE.md)**

In your agent, say:

> "Remember that in this project we always use kebab-case for skill directory names."

Expected behaviour:
- Agent reads the current project `CLAUDE.md` (or notes it doesn't exist)
- Shows a **before/after diff** proposing to add the fact
- Does NOT write until you say "yes"
- After approval: confirms `Memory updated: <path>`

**Test 2b — User-global memory**

> "Going forward, I prefer concise responses without bullet-point overuse. Add this as a global rule."

Expected:
- Agent flags this as **user-global** scope (high impact), asks you to confirm scope
- Targets `~/.claude/CLAUDE.md` (or equivalent)
- Shows diff and waits for approval

**Test 2c — Memory removal with archive**

> "Forget the rule about kebab-case I just added."

Expected:
- Agent shows a diff that comments out the line: `<!-- archived: YYYY-MM-DD: user removed -->`
- Does not silently delete

**Test 2d — Update an existing memory entry**

> "Update my python persona memory — I now use uv instead of pip for dependency management."

Expected:
- Agent reads `development-engineer/persona/python-preferences.md` (or `python.md`) — confirms the file exists
- Shows a before/after diff proposing to add or edit the relevant line
- Does **not** write until you say "yes"
- After approval: confirms `Memory updated: <path>` and updates `last-updated` in frontmatter

> **Gate 2:** Confirm write, scope confirmation, archive, and update flows all behave correctly and require approval at each step.

**Phase 2 notes** _(fill in during testing)_:
- [x] 2a: project memory write triggered diff + approval
- [x] 2b: global memory flagged scope and required confirmation
- [x] 2c: removal used archive comment, did not silently delete
- [ ] 2d: update to existing entry showed diff and required approval
- Findings: global scope routes to `~/.skillmanager/model.md` (not `llm/*.md`); 2a correctly detected existing fact and skipped write

---

## Phase 3 — Memory Skill: Audit + Create + Toggle Workflows

**Goal:** Verify the three memory sub-workflows function as documented.

**Test 3a — memory-audit**

> "Run memory-audit — list all memory files and their contents."

This invokes [`../../skills/brain-manager/workflows/brain-audit.md`](../../skills/brain-manager/workflows/brain-audit.md). Expected:
- Lists project `CLAUDE.md`, user `~/.claude/CLAUDE.md`, any `persona/*.md` files
- Shows their contents or line counts; flags oversized files (>40 lines)

**Test 3b — memory-create (stub scaffolding)**

> "Create a new per-skill memory stub for the `development-engineer` skill, topic: python-preferences."

This invokes [`../../skills/brain-manager/workflows/brain-create.md`](../../skills/brain-manager/workflows/brain-create.md). Expected:
- Proposes creating `development-engineer/persona/python-preferences.md` under your installed skills tree (e.g. `~/.skillmanager/skills/...`)
- Shows the stub content, writes only on approval

**Test 3c — memory-system-toggle**

> "Show me how to toggle the memory skill between always-on and manual modes."

This invokes [`../../skills/brain-manager/workflows/brain-system-toggle.md`](../../skills/brain-manager/workflows/brain-system-toggle.md). Expected:
- Explains the `system-skills-always-on.md` vs `system-skills-manual.md` persona files
- Shows what would need to change, with your approval required before any edit

> **Gate 3:** Confirm all three workflows are reachable and behave correctly.

**Phase 3 notes** _(fill in during testing)_:
- [x] 3a: memory-audit listed all memory files
- [x] 3b: memory-create proposed stub and waited for approval
- [x] 3c: memory-system-toggle explained modes without auto-editing
- Findings: 3a clean — no stale/bloated/orphaned files; I-6 raised (no last-updated on persona files). 3b created python-preferences.md at ~/.skillmanager/skills/development-engineer/persona/, router row added to SKILL.md. 3c correctly explained both modes and identified missing system-skills block in model.md (not present in this install — installer should add it).

---

## Phase 4 — Memory Routing: Per-Skill Persona Files

**Goal:** Validate the persona routing works for existing skills that use `persona/`.

Example source paths in this repo (same layout under `~/.skillmanager/skills/` after install):
- [`../../skills/development-engineer/persona/python.md`](../../skills/development-engineer/persona/python.md)
- [`../../skills/development-engineer/persona/react.md`](../../skills/development-engineer/persona/react.md)

**Test 4a — Read a persona file**

> "Show me the contents of my python persona memory."

Expected: reads `.../development-engineer/persona/python.md` and displays it.

**Test 4b — Update a persona file**

> "Remember, for Python work I prefer type hints on all function signatures. Update my python persona memory."

Expected:
- Memory skill routes to `development-engineer/persona/python.md`
- Shows before/after diff
- Writes only on approval

> **Gate 4:** Confirm persona routing is working. Confirm you are satisfied with how facts are segmented (project vs global vs per-skill).

**Phase 4 notes** _(fill in during testing)_:
- [x] 4a: read `python.md` correctly
- [x] 4b: memory update routed to persona file, showed diff, required approval
- Findings: routing worked correctly; "strict type hints" wording sharpened to "strict type hints on all function signatures" per user preference

---

## Phase 5 — Skill Manager: Skill Health

**Goal:** Use `skill-manager` to audit your installed skills for quality and consistency.

**Test 5a — Skills audit**

> "Run the skills audit workflow — check all active skills for compliance."

This invokes [`../../skills/skill-manager/workflows/skills-audit.md`](../../skills/skill-manager/workflows/skills-audit.md). Expected:
- Iterates through each active skill
- Checks for required front matter (`name`, `description`, `metadata.status`)
- Reports any gaps without auto-fixing

**Test 5b — Review one skill**

> "Review the `memory` skill — is it complete and compliant?"

This invokes [`../../skills/skill-manager/workflows/skills-review-one.md`](../../skills/skill-manager/workflows/skills-review-one.md).

> **Gate 5:** Confirm skill-manager can audit skills and report issues correctly. No fixes needed — just visibility.

**Phase 5 notes** _(fill in during testing)_:
- [x] 5a: skills-audit ran and reported any front matter gaps
- [x] 5b: review-one on `memory` returned a compliance verdict
- Findings: 5a clean after fixes — 7 skills gained ## References sections; 4 persona files gained last-updated frontmatter; `scripts/skills_audit.py` added to codebase; all 16 skills now pass 0 failures

---

## Phase 6 — Knowledge OS Cowork Automations

**Goal:** Verify the three Cowork scheduled task definitions are correctly configured for your environment.

> Pre-condition: you need `OBSIDIAN_ROOT` and `OBSIDIAN_META` set (check `knowledge-os/knowledge-os.env.example`). If Obsidian is not yet set up, skip this phase.

**Test 6a — Environment check**

```bash
skillmanager knowledge-os   # checks OBSIDIAN_ROOT, OBSIDIAN_META, wiki-harvest and vault-paths symlinks
```

Expected: no errors; confirms the two required skills are symlinked.

**Test 6b — Inbox Process task**

Review [`../../knowledge-os/cowork/task-inbox-process.txt`](../../knowledge-os/cowork/task-inbox-process.txt). Steps:
1. Paste the task content into Claude Cowork (or run manually)
2. Set your real `OBSIDIAN_ROOT` and `OBSIDIAN_META` paths in the placeholders
3. Run against a small test inbox (1-2 notes)
4. Confirm it stops after listing pending items and waits for your approval before moving files

**Test 6c — Super Wiki Refresh task**

Review [`../../knowledge-os/cowork/task-super-wiki-refresh.txt`](../../knowledge-os/cowork/task-super-wiki-refresh.txt). Same process — configure paths, run on a test vault, confirm incremental sync and no auto-edits to `meta/wiki/`.

**Test 6d — Wiki Harvest Refresh**

Review [`../../knowledge-os/cowork/task-wiki-harvest-refresh.txt`](../../knowledge-os/cowork/task-wiki-harvest-refresh.txt). Confirm triage of curated pages by status emoji, and that sprint card drafts require your approval.

> **Gate 6:** Confirm at least `skillmanager knowledge-os` passes clean. For each Cowork task, confirm the approval gate works (it stops and waits, does not auto-move/edit).

**Phase 6 notes** _(fill in during testing)_:
- [x] 6a: `skillmanager knowledge-os` passed with no errors
- [x] 6b: inbox-process fully Cowork-driven (Phase A: raw→classified, Phase B: approved→target); classify.sh moved to knowledge-os/scripts/ as manual fallback; flat YAML frontmatter (no routing: wrapper); file processed, classified, and moved to destination — verified
- [ ] 6c: super-wiki-refresh ran incrementally, did not auto-edit `meta/wiki/`
- [ ] 6d: wiki-harvest triage required approval for sprint card drafts
- Findings:

---

## Keeping the plan alive

After completing each phase:
1. Update the **Progress tracker** table above (change `pending` → `done`)
2. Fill in the **Phase N notes** checklist
3. Update the `todos` in the YAML frontmatter of this file to match
4. Commit this file to git so progress is version-controlled:

```bash
git add raw/testing/verification-plan.md
git commit -m "chore: verification plan — phase N complete"
```

If you need to hand off or resume in a new session, use the **Session resume prompt** at the top of this file.

## Summary: Phase Order and Gates

```mermaid
flowchart TD
    P0["Phase 0\nEnvironment Health"] -->|"Gate 0: doctor clean"| P1
    P1["Phase 1\nSkill Symlinks"] -->|"Gate 1: memory visible"| P2
    P2["Phase 2\nMemory Write Flow"] -->|"Gate 2: diff + approval"| P3
    P3["Phase 3\nMemory Workflows"] -->|"Gate 3: audit/create/toggle"| P4
    P4["Phase 4\nPersona Routing"] -->|"Gate 4: per-skill memory"| P5
    P5["Phase 5\nSkill Manager Audit"] -->|"Gate 5: health report"| P6
    P6["Phase 6\nCowork Automations"] -->|"Gate 6: approval gates"| done["Done"]
```

**Signal phrases to use during the session:**
- "Phase N done — move on" → advance to next phase
- "Phase N issue: [description]" → triage before proceeding
- "Skip Phase N" → skip an optional phase (6 is optional if no Obsidian)

---

## Improvement Backlog

Non-blocking improvements identified during testing. Append new items here; promote to a phase only if the item becomes a blocker for testing.

| # | Title | Status | Notes |
|---|-------|--------|-------|
| I-1 | `skillmanager update` command | `pending` | Fetch framework updates from GitHub (tarball strategy), sync install dir, apply renames via `_manifest.json` `formerly` field, run audit. Designed for SaaS: `update_endpoint` and `update_token` in config, swappable from GitHub PAT to subscription key. |
| I-2 | Cross-platform path refactor | `pending` | Replace hardcoded path strings with `pathlib.Path` throughout `skillmanager.py`. Add `link_or_copy()` helper (symlink on macOS/Linux, junction on Windows). Prerequisite for Windows support and choco/winget distribution. |
| I-3 | Compiled binary + package manager distribution | `pending` | PyInstaller binary → Homebrew formula (macOS), `curl \| sh` bootstrap (Linux), choco/winget (Windows). Enables first-class install experience with no Python dependency. Do after I-2. |
| I-4 | Subscription key gate + expiry check | `pending` | `update_token` required to fetch skills. Add `valid_until` field checked at session start — expired key stops skill loading. Enables token revocation. Prerequisite for Rings 2–4 of IP protection. Do after I-1. |
| I-5 | Vendor / user overlay layer model | `pending` | Split install into `~/.skillmanager/skills/` (vendor, read-only, managed by update) and `~/.skillmanager/overrides/` (user, writable, never touched by update). LLM sees merged view; override wins on conflict. `skillmanager update` never modifies overrides. `skill-manager` skill routes edits to correct layer. Requires changes to `skillmanager.py`, `install.py`, and `skills-create.md`. |
| I-6 | `last-updated` frontmatter on persona files | `pending` | None of the persona files (`development-engineer/persona/*.md`, `wiki-harvest/persona/*.md`) carry a `last-updated` field, making automatic staleness checks (>90 days) impossible. Add `last-updated: YYYY-MM-DD` to persona frontmatter and update the `memory-create` scaffold to include it by default. |
| I-7 | Research alternative backends to Obsidian | `pending` | The Knowledge OS Cowork automation layer is tightly coupled to Obsidian as the vault backend (OBSIDIAN_ROOT, OBSIDIAN_META). Research alternative backends (e.g. Notion, Logseq, plain markdown dirs, Foam) and document requirements for a backend-agnostic adapter layer so the skill works without Obsidian. |
| I-8 | Example user guide from verification test results | `pending` | Distill Phases 0–3 test cases (environment check, skill visibility, memory write/update/archive/audit/create/toggle) into a short "quick-start test guide" document aimed at first-time installers. Scope: run before starting a real project; covers the happy path only; links back to this plan for edge cases. |
| I-9 | Auto-cleanup orphaned skills on audit | `done` | `formerly` field added to `brain-manager/SKILL.md`. `skillmanager audit` now auto-removes orphan symlinks that match a `formerly` entry; unknown orphans still flagged for manual review. `--dry-run` flag added to audit. `skillmanager update` removes old skill dirs on rename. 4 new tests added, all passing. |
| I-10 | Merge `core/ingest.md` into Skillforge | `pending` | Raw→research pipeline from choreokit. Depends on domain skills (bible-study, product, etc.) being live and validated. Adds `op: ingest` to all domain master skills. |
| I-11 | Merge `core/schema-sync.md` into Skillforge | `pending` | Graph/schema sync skill from choreokit. Depends on `schema/entities.json` vault convention being adopted. |
| I-12 | Merge `classify/concierge.md` into Skillforge | `pending` | Conversational capture skill from choreokit. Could become a Cowork task (`task-concierge.txt`) or a standalone skill. Trigger: `op: concierge` or `capture this:`. |

Status values: `pending` → `in-progress` → `done` or `deferred: <reason>`
