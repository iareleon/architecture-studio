---
name: git-manager
version: 1.0.0
description: Handle Git operations, including status, diffing, and automated commit message generation.
---
## Core Responsibilities
- **Status & Monitoring:** Check the current state of the repository (staged vs unstaged changes).
- **Diff Analysis:** Perform comprehensive `git diff` to understand code changes.
- **Commit Management:** Generate high-quality, "why"-focused commit messages based on `git diff` analysis.
- **Terminal Integration:** Execute git commands directly via terminal when necessary.

## Workflow
1. **Status:** Always start by running `git status` to see the current state.
2. **Review:** Run `git diff HEAD` (and `git diff --staged` if applicable) to gather technical context of all changes.
3. **Draft:** Propose a concise and descriptive commit message based on the diff.
4. **Commit:** Upon user approval, stage the files (`git add`) and commit (`git commit`).
5. **Verify:** Run `git status` again to confirm the commit was successful.

## Automation & Guardrails

- **Commit Preparation:** Run `node scripts/prepare_commit.cjs` to capture local changes and scaffold a summary task for the LLM.
- **LLM Integration:** Once scaffolded, prompt the LLM to "Process the pending commit in llm/changes/YYYY-MM-DD-HH24-MM-staged-changes-summary.md".
