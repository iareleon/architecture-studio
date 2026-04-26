# SkillsLoom

[![Validate](https://github.com/Choreogrifi/skill-manager/actions/workflows/validate.yml/badge.svg)](https://github.com/Choreogrifi/skill-manager/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-SkillsLoom-blue)](https://choreogrifi.github.io/skill-manager/)

**SkillsLoom gives your AI assistant a permanent memory and a set of expert skills, so it does better work and costs less to run.**

---

## What it does

- **Remembers you.** Tell the AI your preferences once — your tech stack, working style, code standards — and it remembers them across every session. No more repeating yourself.
- **Works like a specialist.** Activate a skill and your AI immediately knows the deep conventions for that domain: Git hygiene, Terraform patterns, security reviews, technical writing, and more.
- **Loads only what it needs.** Skills and memory are loaded on demand and unloaded when done. You never pay tokens for context you are not using.

**System of record:** your configured knowledge base (wiki, vault, or doc system) holds canonical knowledge. Bundled skills **augment** you — conventions, checklists, and drafts for your review — not a separate automation silo in parallel with that structure.

**UAT and scope:** validate the framework by driving work from a terminal with **Claude CLI** (step-by-step, with human approval where skills require it). **Scheduled or product automation is intentionally out of scope until UAT passes**; after that, automation can be layered on the same procedures already encoded in the skill library. For day-to-day use of every skill under `skills/`, see **[PLAYBOOK.md](PLAYBOOK.md)**.

---

## Install in 30 seconds

**Homebrew (macOS / Linux):**
```bash
brew tap choreogrifi/skill-manager && brew install skill-manager
```

**curl one-liner:**
```bash
curl -fsSL https://raw.githubusercontent.com/Choreogrifi/skill-manager/main/scripts/install.py | python3
source ~/.zshrc
```

The installer asks which AI tools you use (Claude, Gemini), detects your installed tools (git, gh, gcloud, terraform), and sets everything up.

---

## Three quick examples

**1. Git expertise on demand**
```
User:   I need to resolve a merge conflict in src/api/handler.ts

With git active:
AI:     Reads both sides of the conflict, explains the trade-off,
        proposes the resolved content, and waits for your approval
        before writing.
```

**2. Infrastructure scaffolding**
```
User:   Add a new serverless job for the order processor

With the `devops-engineer` skill active:
AI:     Discovers your existing Terraform folder, reads your naming
        conventions, drafts the full HCL module, and confirms before
        writing a single file.
```

**3. Content in your voice**
```
User:   Write a LinkedIn post about our new open-source release

With `social-media-manager` active:
AI:     Asks for your audience and tone, drafts a post in your brand
        voice with the right LinkedIn formatting, and iterates until
        you approve.
```

---

## How it works

**Skills** are small text files that tell the AI what to focus on and how to behave. Each skill’s `SKILL.md` can set `metadata.status` (default `active`). `skillmanager audit` creates or removes symlinks in your AI tool’s skills directory so only the skills you want are visible. No skill files are deleted when you change status.

**Memory files** are separate documents that hold things the AI should remember about you: your role, your project conventions, your preferences. They are loaded at session start and written only when you explicitly say "remember this." They stay small because every line you load costs tokens.

```bash
skillmanager ls          # see each skill’s metadata.status and symlink health
# set metadata.status in skills/<name>/SKILL.md, then:
skillmanager audit       # align symlinks with status (or: skillmanager sync)
skillmanager doctor      # check your environment
```

---

## Skill catalogue

Each **skill** is one directory under `skills/<name>/` (routers with `workflows/`; no separate `-sme` / `-wf` installs). The **canonical list**, descriptions, and workflow entry points for the current repo are in **[PLAYBOOK.md](PLAYBOOK.md)** (covers `skills/` only).

---

## Personalise it

After install, use the **`brain-manager`** skill to build up memory as you work:

```bash
# See what memory files are loaded and their token cost
skillmanager memory-help
```

Keep memory files focused. Every line you add is loaded into every session.

---

## Contribute

1. Fork the repository
2. Create a branch: `git checkout -b feat/add-<skill-name>`
3. Add or edit skills following the [Skill Spec](https://choreogrifi.github.io/skill-manager/skill-spec)
4. Validate: `python3 scripts/check_skill_names.py && skillmanager audit`
5. Run tests: `pytest tests/test_skillforge.py -v`
6. Open a pull request — CI validates all SKILL.md files automatically

New skills must be generic (no personal data, no hardcoded paths) and follow the single-responsibility principle. See `skills/README.md` for full guidelines.

---

[MIT License](LICENSE) — [Documentation](https://choreogrifi.github.io/skill-manager/) — [Report an issue](https://github.com/Choreogrifi/skill-manager/issues)