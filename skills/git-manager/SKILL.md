---
name: git-manager
description: Git and GitHub/GitLab — router. Load workflows for provider, local git, or commit automation. Invoke for any repository operation.
metadata:
  version: "1.0"
  disable-model-invocation: true
---
# Git (router)

**Main brain:** this file. Command patterns: `references/expertise.md`, `references/github-operations.md`, `references/gitlab-operations.md`. Load **one** matching workflow; do not read every subflow at once.

| If… | Open |
|-----|------|
| **GitHub** remote or user said GitHub | `workflows/github-platform.md` + `references/github-operations.md` |
| **GitLab** or user said GitLab | `workflows/gitlab-platform.md` + `references/gitlab-operations.md` |
| Unclear / no `origin` | `workflows/provider-routing.md` |
| **Commit** message from staged diff | `workflows/commit-automation.md` |
| Clone, branch, tag, conflict, `git all`, create repo | match `workflows/git-*.md` |

**Always before risky ops:** `git status` and recent context; **explicit approval** before reset/rebase/remote changes; **no** force-push to default branch; **no** `--no-verify` unless the user asks.

## Conventions (summary)

- Default branch: `main`. Branches: `<type>/<ticket>-<description>` with types `feat`, `fix`, `chore`, `docs`, `refactor`, `test`.
- **Commits:** Conventional `feat:`, `fix:`, `chore:`, etc.; atomic; never commit credentials, `.env`, or large generated binaries. Subject ≤72 chars, imperative; body explains why; `git add` specific paths—watch untracked.
- **Merge:** rebase before PR when team agrees; squash only for noisy WIP; never force-push `main` / `master`.
- **PR/MR:** conventional title; body with summary, test plan, checklist; squash merge common for features; pipeline green before merge (GitLab: no bypass).

## Provider routing

- `git remote get-url origin` → GitHub vs GitLab. Destructive or remote-affecting actions: dry-run summary + explicit approval. GitHub: `gh`; GitLab: `glab` for platform ops.

## Commit helper (automation)

- Run `git status`, `git diff HEAD`, `git log -n 3` for context. Match message to project conventions. Approve before commit. No `--no-verify` / `--no-gpg-sign` unless requested.

For full copy-paste command patterns, use the references above.
