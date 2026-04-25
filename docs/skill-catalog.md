---
title: Skill Catalog
---

# Skill Catalog

All built-in skills included with skill-manager. Skills are organised into two categories:
**SME** (Subject Matter Expertise) and **Workflow**.

**Layout:** Each skill’s canonical rules live in **`SKILL.md`**. Optional deep references in `references/`; optional sub-topics in **`persona/`**. Project-specific context belongs in workspace **`CLAUDE.md`**, not per-skill `memory/baseline.md`.

---

## SME Skills

SME skills give the AI deep domain knowledge. When active, the AI applies the skill's standards and constraints to every response in the session.

| Skill | Domain | Main brain | Related skills |
|---|---|---|---|
| `architect` | Systems, solution, and enterprise architecture — Hexagonal/Clean, ADRs, C4, cross-vertical validation | `SKILL.md` | `documenter` (HLD templates) |
| `development-engineer` | Software implementation — shared rules in `SKILL.md`; stacks in `persona/python.md`, `persona/react.md` | `SKILL.md` + `persona/` | `security` |
| `devops` | IaC, CI/CD, Terraform, Cloud Build, observability | `SKILL.md` + `workflows/`, `references/` | `security`, `cloud-engineer` |
| `security` | IAM, secrets, OWASP, vulnerability assessment | `SKILL.md` | `architect`, `development-engineer` |
| `tester` | Test strategy, TDD, unit/integration tests | `SKILL.md` | — |
| `git` | Git concepts — branching, commits, conflicts, history | `SKILL.md` + `references/expertise.md` | — |
| `cloud-engineer` | Google Cloud Platform — resources, IAM, managed services; gcloud inventory | `SKILL.md` | — |
| `diagrammer` | Diagram type selection; Mermaid maintenance conventions | `SKILL.md` | `diagrammer` |
| `documenter` | Technical writing — READMEs, HLDs, ADRs; requirements and research synthesis | `SKILL.md` | `diagrammer` |
| `skill-manager` | Creating, auditing, and governing skills | `SKILL.md` + `workflows/`, `references/` | `skill-manager` |
| `social-media` | Social media, video scripts, written guides; prompt precision | `SKILL.md` | — |

---

## Workflow Skills

Workflow skills automate multi-step processes with a confirmation gate before any irreversible action. They load additional **workflow** files from `workflows/*.md` on demand (see [Domain layout](domain-layout.md)).

| Skill | What it automates | Example `workflows/` files | Related skills |
|---|---|---|---|
| `git` | Routes git operations to GitHub or GitLab | `git-clone`, `git-branch`, `git-conflict`, `git-tag` | — |
| `git` | GitHub: PRs, releases, issues, branches via `gh` | `github-pr`, `github-release` | — |
| `git` | GitLab: MRs, pipelines, branches via `glab` | `gitlab-mr`, `gitlab-pipeline` | — |
| `documenter` | Create, review, update, or extend documents; HLD scaffold library | `documenter-readme`, `documenter-audit`, `documenter-update`, `documenter-extend`, `documenter-adr` | `documenter`, `diagrammer` |
| `diagrammer` | Generate, validate, and improve Mermaid diagrams | `mermaid-write`, `mermaid-read`, `mermaid-improve` | — |
| `devops` | Terraform HCL: scaffold, scan, conventions (merged former `terraform` skill) | `terraform-scan`, `terraform-main` | `cloud-engineer` |
| `cloud-engineer` | Inventory existing GCP resources via `gcloud` | `cloud-discover`, `cloud-scan` | — |
| `skill-manager` | Create, audit, propose, and refine skills | `skills-create`, `skills-detect`, `skills-audit`, `skills-propose`, `skills-refine` | `memory` |
| `memory` | Propose diffs to project `CLAUDE.md`, `persona/`, or legacy per-skill memory; discovery scaffolding; librarian templates | `memory-create`, `memory-audit`, `memory-system-toggle` | — |
| `social-media` | Social posts, video scripts, and written guides | `social-media-posts`, `social-media-video` | `social-media` |
| `personal` | Drift checks, track alignment, meeting notes, decision logs, soul-layer capture | `personal-daily`, `personal-drift`, `personal-review`, `personal-soul-write` | `vault-paths` |
| `wiki-harvest` | Brain dump → wiki; `persona/meridian.md` (Meridian) · `persona/knowledge-os.md` (meta) | `wiki-harvest-session`, `wiki-harvest-sprint` | `vault-paths` |
| `vault-paths` | Multi-vault path resolution and write rules | (router in `SKILL.md`) | — |
| `project-manager` | ClickUp task routing | `project-manager-create` (+ query/update/sprint when present) | — |

---

## Managing Skills

```bash
# List all skills: metadata.status vs symlinks
skillmanager ls

# Change metadata.status in skills/<name>/SKILL.md, then align symlinks:
skillmanager audit
```

See the [CLI Reference](cli.md) for the full command list.

---

## Creating a New Skill

```bash
# SME (expertise) skill
cp skills/skill-manager/templates/expertise-skill-template.md skills/<your-skill>/SKILL.md

# Workflow skill
cp skills/skill-manager/templates/workflow-skill-template.md skills/<your-skill>/SKILL.md

# Workflow fragment (under a workflow skill)
cp skills/skill-manager/templates/workflow-fragment.md skills/<parent>/workflows/<workflow-name>.md
```

Fill in the placeholders, set `name:` to match the folder name (e.g. `name: my-skill`), set `metadata.status: active` (or omit; default is active), then:

```bash
skillmanager audit
```

See the [SKILL.md Specification](skill-spec.md) for the full format reference.
