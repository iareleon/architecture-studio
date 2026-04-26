# SkillsLoom playbook — `skills/` only

This document describes how to **use the framework through the skill library** shipped in this repository’s `skills/` directory. It does **not** document installers, CI, Knowledge OS vault layout, or third-party bundles outside `skills/`.

---

## Operating model (UAT phase)

- **Primary interface:** run work in a terminal with **Claude CLI** (or any client that loads the same skill files). You drive each flow step by step; the agent follows the active skill’s `SKILL.md` and linked workflows.
- **Human approval:** skills that change memory, move vault files, or rewrite canonical docs are written to **stop for confirmation** where the skill says so. Treat that as part of UAT, not optional polish.
- **Automation:** scheduled runners, product-specific daemons, and similar **are out of scope until UAT passes**. After UAT, automation can be scoped on top of the same procedures already encoded in `skills/` (no parallel “shadow” process).

Symlinks from your install (e.g. `~/.claude/skills/<name>` → your configured `skills/<name>/`) are managed by **`skillmanager audit`** after you change `metadata.status` in each `SKILL.md`. Install and CLI details live in the root [README](README.md); this playbook stays inside `skills/`.

---

## Layout and conventions

- **One skill = one directory:** `skills/<skill-name>/` (kebab-case; `name` in front matter must match the folder).
- **Router:** `SKILL.md` is usually the entry point: description, rules, and a table of **workflows** or routing hints.
- **Supporting material:** optional `workflows/`, `references/`, `persona/`, `templates/`, `scripts/` — load only what the router points to.
- **Lifecycle:** `metadata.status` in `SKILL.md` is typically `active`, `staging`, `review`, `deactivated`, or `decommissioned`. Inactive skills should not have production symlinks.
- **`metadata.formerly`:** optional rename trace (e.g. `formerly: architect`). Useful when searching git history or old notes.
- **`metadata.disable-model-invocation`:** when `true`, the product may not auto-suggest the skill; **attach or invoke it explicitly** when you need that expertise.
- **`:sl` commands:** in domain vault skills, invocations use the **`:`** + **`sl`** prefix (e.g. `:sl research {topic}`) instead of the older `op:` spelling. Treat `:sl` as the short trigger for SkillsLoom-routed vault operations.

Authoring and naming rules: [skills/README.md](skills/README.md). Spec for front matter: [docs/skill-spec.md](docs/skill-spec.md) (outside `skills/`, but referenced by the skill library).

---

## How to work a task (happy path)

1. **Pick the skill** from the catalogue below (or use `skill-manager` to find gaps).
2. **Attach / enable** that skill in your CLI session (per Claude CLI behavior).
3. **Open** `skills/<name>/SKILL.md` and follow the router to the right `workflows/*.md` file.
4. **Execute** the workflow: answer prompts, run commands the workflow lists, and approve diffs when required.
5. **Cross-skill:** routers often point to another skill (e.g. `wiki-manager` for Knowledge OS ops, `cloud-engineer` with `devops-engineer`). Switch attachment or load the linked file as needed.

---

## Catalogue (all skills under `skills/`)

| Directory | Purpose (from `description`) |
|-----------|------------------------------|
| `architect-manager` | Solution and systems architecture — NFRs, trade-offs, C4, ports/adapters, and secure-by-default design. Use when the user asks how to structure a system, which pattern fits, whether a design is over-engineered, what to build vs buy, or to review a proposal, ADR, or integration boundaries — even if they do not say "architecture" or "HLD." |
| `bible-study-manager` | Bible-study Obsidian vault — passage research, cross-references, theme synthesis, study guides, and promotion to the wiki. Use when the user wants to work a passage, build a study outline, track themes, prep teaching notes, or move notes from raw to wiki — even if they only say things like "I read this in Romans" or "help me turn this into a study." |
| `brain-manager` | Workspace memory and project convention updates — map intent to the right memory file, draft changes, and apply only with explicit user approval. Use when the user says things like "remember that...", "update CLAUDE.md", "I decided we will...", "make this the default", or "note that for the project" — even if they do not say "memory." |
| `business-manager` | Business Obsidian vault — strategy research, market/competitive notes, client briefs, and promotion to the wiki. Use when the user is capturing deals, writing positioning, building a case, or needs anything promoted from the business vault — even if they call it a "work note" or a "meeting follow-up." |
| `cloud-engineer` | Read-only cloud discovery and inventory (e.g. GCP) — what exists, where it lives, and a sensible SME snapshot for defaults. Use when the user asks what is in a project, how resources are named, to scan or list services, to compare as-is to a design, or to baseline infra before a change — even if they only paste a gcloud error or a resource name. |
| `development-engineer` | Software implementation — SOLID, DI, strict typing, tests aligned with the stack, and honest trade-offs. Use when the user wants code written, a feature implemented, a refactor, a PR prepped, project setup, or a review of structure and boundaries — even if they just paste a file or say "fix this." |
| `devops-engineer` | DevOps and IaC — CI/CD, Terraform, modules, remote state, pipelines, and HCL/scan workflows; pair with `cloud-engineer` for live cloud inventory. Use when the user asks to fix a pipeline, write a workflow, set up GitHub Actions, wrangle state, or scaffold Terraform — even if they say "the deploy is broken" without naming the tool. |
| `diagram-manager` | Diagrams — Mermaid and diagram-type guidance (flow, sequence, state, ER, C4). Use when the user wants to draw, sketch, "show me the flow", drop a mermaid block in a doc, or pick the right chart type — even if they only say "visualise this" or paste bullet points. |
| `document-manager` | Technical writing — README, ADR, HLD, document audits, and structured updates. Use when the user needs a new doc from a template, a spec or ADR, a long-form HLD, a doc pass before release, or a refresh of an existing file — even if they say "we need a doc for this" or "formalise this in writing." |
| `engineering-manager` | Engineering Obsidian vault — feature specs, design notes, ADRs, and promotion to the wiki. Use when the user is drafting a feature, recording a technical decision, or moving engineering material into the wiki — even if the note lives under a scratch path or a daily log first. |
| `git-manager` | Git and hosting — local git, GitHub, GitLab; commits, branches, PRs/MRs, releases, and conflict resolution. Use when the user says commit, rebase, merge conflict, open a PR, tag a release, clone, rename a repo, or needs provider-specific steps — even if they only paste `git` output or a GitHub link. |
| `hobbies-manager` | Hobbies Obsidian vault — photography (shoots, reviews, technique), gear notes, and promotion to the wiki. Use when the user logs a session, rates shots, plans gear, or curates creative work into the wiki — even if the note is a quick field capture without "hobby" in the title. |
| `personal-manager` | Focus, drift checks, and meeting/decision capture for project work; optional soul-style reflective notes if configured via `wiki-manager`. Use when the user says they feel scattered, want alignment ("am I on track?"), need meeting actions or a decision log, or asks for a reflective / soul note path — even if they only tag #focus or dump a brain dump of worries. |
| `product-manager` | Product Obsidian vault — idea research, viability, competitive framing, design imports, and promotion to the wiki. Use when the user is shaping a bet, a PRD sketch, a customer problem, or moving product thinking into the wiki — even if the file is a rough note in `raw/` with no product jargon. |
| `project-manager` | Create, update, and query work in the configured task tool; route blockers, sprint items, and proposals to the right list. Use when the user says track this, add a card, what is blocked, move it to the sprint, or file a follow-up for the team — even if they never name Linear/Jira/Asana and only describe a next step. |
| `security-manager` | Security reviews — secrets hygiene, IAM/RBAC, OWASP-style code and config checks, and threat thinking at boundaries. Use when the user asks if something is safe, to scan for hardcoded creds, to tighten permissions, to review a PR for security, or to assess a design before go-live — even if they only say "I am worried about this endpoint" or paste an IAM policy. |
| `skill-manager` | Create, audit, refine, and lifecycle-manage skills under `skills/`. Use whenever the user wants to create a new skill, scaffold a `SKILL.md`, capture a repeatable workflow as a skill, check whether a skill exists for a task, review or improve an existing skill, detect gaps in the skill library, audit skill quality or naming, propose a skill to the repository, or asks anything like "can you make a skill for this?", "do I have a skill that does X?", "review my skills", or "let's improve this skill". Trigger even when the user describes a workflow they want to capture — that's a skill creation opportunity. |
| `social-media-manager` | Public-facing social and long-form content — short posts, threads, video scripts, and guides. Use when the user wants a draft for X/LinkedIn/Threads/Bluesky/Instagram, a script or shot list, a content calendar, or a how-to article — even if they only say "make this a post" or drop rough bullets. |
| `test-manager` | Testing strategy and test code — pyramids, unit vs integration, naming, and CI expectations aligned with the stack. Use when the user asks for tests, "how do I test this?", better coverage, a failing suite, or a review of assertions on a PR — even if they only share a function and a bug report. |
| `wiki-manager` | Knowledge OS — config, inbox pipeline, dispatch between meta and vaults, wiki and structure sync, harvest sessions, and sprint cards from wiki. Use for anything like process my inbox, move this note to a vault, refresh the super-wiki, run a harvest, or set up `wiki-manager.config` — when in doubt, route knowledge-base work here even if the user says "put this in the wiki" without naming the tool. |

---

## Entry points and workflows (by skill)

Use each row as a map from **directory** → **first file to open** → **main workflows** (paths relative to `skills/<directory>/`).

| Directory | Open first | Main workflows / notes |
|-----------|------------|-------------------------|
| `architect-manager` | `SKILL.md` | Main brain only; principles and security baseline in `SKILL.md`. |
| `bible-study-manager` | `SKILL.md` | `workflows/passage-research.md`; promotion steps reference `wiki-manager` sync. |
| `brain-manager` | `SKILL.md` | `workflows/brain-create.md`, `brain-audit.md`, `brain-system-toggle.md`. |
| `business-manager` | `SKILL.md` | Vault ops; follow `SKILL.md`; wiki promotion pairs with `wiki-manager`. |
| `cloud-engineer` | `SKILL.md` | `workflows/cloud-inventory.md`; `references/gcloud-discovery-commands.md`. |
| `development-engineer` | `SKILL.md` | Main brain only; stack and TDD rules in `SKILL.md`. |
| `devops-engineer` | `SKILL.md` | `workflows/terraform-scan.md`, `workflows/terraform-main.md`. |
| `diagram-manager` | `SKILL.md` | `workflows/mermaid.md`; `references/output-patterns.md`. |
| `document-manager` | `SKILL.md` | `workflows/documenter-menu.md`; analyst templates under `references/analyst-templates/`. |
| `engineering-manager` | `SKILL.md` | Vault ops; follow `SKILL.md`; wiki promotion pairs with `wiki-manager`. |
| `git-manager` | `SKILL.md` | `workflows/github-platform.md`, `gitlab-platform.md`, `provider-routing.md`, `commit-automation.md`. |
| `hobbies-manager` | `SKILL.md` | Vault ops; follow `SKILL.md`; wiki promotion pairs with `wiki-manager`. |
| `personal-manager` | `SKILL.md` | `workflows/personal-daily.md`, `personal-drift.md`, `personal-review.md`, optional soul flows; vault ops `workflows/vault-*.md`. |
| `product-manager` | `SKILL.md` | `workflows/design-import.md`; wiki promotion pairs with `wiki-manager`. |
| `project-manager` | `SKILL.md` | `workflows/project-manager-create.md`, `project-manager-query.md`, `project-manager-update.md`, `project-manager-sprint.md`. |
| `security-manager` | `SKILL.md` | Main brain only; audit order and standards in `SKILL.md`. |
| `skill-manager` | `SKILL.md` | `workflows/skill-manager-menu.md`, `skills-create.md`, `skills-audit.md`, `skills-review-one.md`, `skills-detect.md`, `skills-propose.md`, `skills-refine.md`. |
| `social-media-manager` | `SKILL.md` | `workflows/social-media-menu.md`, `social-media-posts.md`, `social-media-video.md`; vault ops `workflows/vault-*.md`. |
| `test-manager` | `SKILL.md` | Main brain only; strategy and naming in `SKILL.md`. |
| `wiki-manager` | `SKILL.md` | `workflows/wiki-manager-config.md`, `inbox-classify.md`, `inbox-dispatch.md`, `vault-inbox-sync.md`, `wiki-sync.md`, `folder-structure-sync.md`, `wiki-harvest-session.md`, `wiki-harvest-sprint.md`. |

---

## New skills and changes

- Use **`skill-manager`** (`workflows/skills-create.md`, `skills-audit.md`) so new directories stay compliant with naming and front matter.
- Run **`python3 scripts/check_skill_names.py`** and **`skillmanager audit`** from the repo root before you merge (installer/CLI; not duplicated here).

---

## Scope reminder

Everything above is intentionally limited to **`skills/`** in this repository. For install, GitHub Pages docs, and repo-wide testing, see the root [README](README.md) and `docs/`.
