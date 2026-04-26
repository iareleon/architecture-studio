---
title: CLI Reference
---

# CLI Reference

## Environment

| Variable | Default | Description |
|---|---|---|
| `SKILLSLOOM_DIR` | `~/.skillsloom` | Skill root directory (read from `~/.skillsloom/config.yaml`) |
| `OBSIDIAN_ROOT` | `~/Obsidian` | Used by `skillmanager knowledge-os` (Obsidian base path) |
| `OBSIDIAN_META` | `~/Obsidian/meta` | Master Knowledge OS vault path |
| `CHOREOKIT_DIR` | (unset) | Optional; separate op-skills tree, reported by `knowledge-os` if set |

Override for safe testing:
```bash
SKILLSLOOM_DIR=/tmp/sf-test skillmanager <command>
```

---

## `skillmanager ls`

List every skill with `metadata.status` (from `SKILL.md`) and whether symlinks on disk look healthy.

```bash
skillmanager ls
```

**Output columns:**

| Column | Values |
|---|---|
| SKILL | Skill name |
| STATUS | `active` (or omitted default), `staging`, `review`, `deactivated`, `decommissioned` |
| SYMLINKS | `ok` / `MISSING` / `STALE` / `-` / staging variants |

Edit `metadata.status` in `skills/<name>/SKILL.md`, then run `skillmanager audit` to update symlinks.

---

## `skillmanager status`

Check that symlinks under `~/.claude/skills` (and configured paths) match each skill’s `metadata.status`. Exits non-zero if anything is out of sync.

```bash
skillmanager status
```

---

## `skillmanager audit` / `skillmanager sync`

Recreate or remove LLM symlinks from each skill’s `metadata.status` (default `active`). `sync` is an alias for `audit`.

```bash
skillmanager audit
skillmanager sync
```

**What it does**

1. For `status: active` (or omitted): ensure production symlinks; remove any staging symlinks for that skill.
2. For `status: staging`: production symlinks removed; `skills-staging` symlinks created.
3. For `review`, `deactivated`, or `decommissioned`: all production and staging symlinks for that skill removed.
4. **Orphan symlinks** in LLM dirs with no `skills/<name>/` are reported.
5. **SKILL.md** frontmatter checks and **context.md** regen for `active` skills with `workflows/`.

There are no `activate` / `deactivate` / `review` / `rm` subcommands: change status in YAML, then `audit`.

---

## `skillmanager doctor`

Self-check the environment for configuration issues.

```bash
skillmanager doctor
```

**Checks:**

- Config file (`~/.skillsloom/config.yaml`) exists
- Install directory exists
- Skills directory exists and is writable
- LLM target directories exist
- `skillmanager` binary is on PATH
- Tool availability (`git`, `gh`, `glab`, `gcloud`, `terraform`)
- Bash version ≥ 4.0

---

## `skillmanager knowledge-os`

Check that the **Obsidian meta** master vault exists, expected paths are present, and that **wiki-manager** (and related Knowledge OS skills) are symlinked in `~/.claude/skills` after `skillmanager audit`. If `CHOREOKIT_DIR` is set, verifies that directory exists.

```bash
skillmanager knowledge-os
OBSIDIAN_ROOT=/path/to/Obsidian skillmanager knowledge-os
```

**See also:** [Knowledge OS + Obsidian meta](knowledge-os.md)

---

## `skillmanager memory-help`

Print a guide to memory files, loading rules, and token cost implications.

```bash
skillmanager memory-help
```

---

## `skillmanager config`

Show or update the current configuration.

```bash
skillmanager config                      # show config.yaml
skillmanager config set user.email me@example.com  # update a value
```

---

## `skillmanager version`

Print the installed version.

```bash
skillmanager version
```

---

## Git Commands

_Available since skillmanager 2.0.0_

`skillmanager git` wraps standard git operations with two safety gates:

1. **Skill naming check** — before `commit`, if any staged files are under `skills/`, all staged skill directory names are validated against the naming standard (`<name>-(sme|wf)`). The commit is blocked if violations are found.
2. **Force-push protection** — before a force-push to `main` or `master`, explicit confirmation is required.

All other subcommands are passed directly to `git`, so the full git command set is available.

### `skillmanager git status`

```bash
skillmanager git status
```

### `skillmanager git log`

```bash
skillmanager git log --oneline -10
```

### `skillmanager git diff`

```bash
skillmanager git diff           # unstaged changes
skillmanager git diff --staged  # staged changes
```

### `skillmanager git add`

```bash
skillmanager git add skills/my-skill/SKILL.md
```

### `skillmanager git commit`

Diff-driven commit flow — always shows the staged diff before asking for a message:

1. Fails with a hint if nothing is staged.
2. Runs the skill naming gate if any staged files are under `skills/`.
3. Prints `git diff --cached --stat` and the full diff.
4. Prints the last 5 commits for style reference.
5. Prompts: `Enter commit message (review the diff above):`
6. **Validates** the message against [conventional commits](https://www.conventionalcommits.org/) format (`feat:`, `fix:`, `chore:`, etc.) as defined in `git`. Non-blocking — warns and asks to proceed if the format is not followed.
7. Confirms the message before committing.

```bash
skillmanager git add scripts/skillmanager.sh
skillmanager git commit
# → shows diff, prompts for message, confirms, then commits
```

### `skillmanager git all`

Stages all modified tracked files, runs the diff-driven commit flow, then pushes — in a single guided sequence.

1. Shows `git status`.
2. If nothing staged, lists modified tracked files and asks for confirmation to stage them.
3. Runs `git diff --cached` and prompts for a commit message (same as `skillmanager git commit`).
4. Confirms the commit.
5. Asks to push to `origin/<current-branch>`.

```bash
skillmanager git all
```

---

### `skillmanager git push`

Passes through to `git push`. Blocks unconfirmed force-push to `main` or `master`.

```bash
skillmanager git push origin feat/my-branch
skillmanager git push --force origin feat/my-branch   # requires confirmation if target is main/master
```

### `skillmanager git pull`

```bash
skillmanager git pull
```

### `skillmanager git branch`

```bash
skillmanager git branch                          # list branches
skillmanager git branch feat/my-skill           # create branch
skillmanager git branch -d feat/merged-branch   # delete branch
```

### `skillmanager git checkout`

```bash
skillmanager git checkout feat/my-branch
skillmanager git checkout -b feat/new-branch
```

### `skillmanager git clone`

```bash
skillmanager git clone https://github.com/org/repo.git
```

### `skillmanager git tag`

```bash
skillmanager git tag v1.0.0
skillmanager git tag -l
```

### `skillmanager git pr`

Create a GitHub pull request. Requires `gh` CLI and `gh auth login`.

```bash
skillmanager git pr --title "feat(skills): add my-skill" --body "Adds new skill."
skillmanager git pr                      # interactive mode
```

### `skillmanager git mr`

Create a GitLab merge request. Requires `glab` CLI and `glab auth login`.

```bash
skillmanager git mr --title "feat(skills): add my-skill" --description "Adds new skill."
skillmanager git mr                      # interactive mode
```

### `skillmanager git repo-create`

Interactively creates a new GitHub or GitLab repository and wires up the local remote.

1. Detects provider from `origin` remote URL, or asks.
2. Prompts for name, visibility (private default), and optional description.
3. Confirms before creating.
4. Creates via `gh repo create` (GitHub) or `glab repo create` (GitLab).
5. Sets or updates `origin` remote to the new URL.
6. Offers to push the current branch.

```bash
skillmanager git repo-create
```

Requires `gh` for GitHub or `glab` for GitLab, and an active auth session.

---

### `skillmanager git repo-rename`

Renames the repository on the platform and updates the local `origin` remote URL in one step.

1. Reads `origin` remote to detect provider, owner, and current name.
2. Prompts for the new name.
3. Derives the new remote URL (preserving SSH or HTTPS protocol).
4. Confirms before proceeding.
5. Renames via `gh repo rename` (GitHub) or `glab api` PATCH (GitLab).
6. Runs `git remote set-url origin <new-url>` and verifies with `git remote -v`.

```bash
skillmanager git repo-rename
```

---

### Pass-through

Any git subcommand not listed above is passed directly to `git`:

```bash
skillmanager git stash
skillmanager git rebase -i HEAD~3
skillmanager git cherry-pick abc1234
```

---

## `skillmanager uninstall`

Interactively removes SkillsLoom from the system. Requires typing `uninstall` to confirm.

```bash
skillmanager uninstall
```

**Steps performed:**

1. **Symlinks** — removes all skill symlinks from `~/.claude/skills/` and `~/.gemini/skills/`.
2. **Binary** — removes `~/.local/bin/skillmanager`.
3. **Skill data** (optional, second confirmation) — removes `$SKILLSLOOM_DIR` including all skills, memory files, and `config.yaml`.
4. **PATH entries** (optional) — removes the `export PATH` line added to `~/.bashrc` / `~/.zshrc` by the installer.

Skill data is never deleted unless you explicitly answer `yes` to the separate confirmation in step 3. This means an uninstall followed by a reinstall preserves all your skills.

> **Note**: The install script rejects git repositories as `SKILLSLOOM_DIR`. If you see an error at install time, choose a path outside any cloned repo (e.g. `~/.skillsloom`).

---

## `skillmanager show <name>`

Display the `SKILL.md` content for any installed skill — frontmatter summary followed by the full body.

```bash
skillmanager show git-manager
skillmanager show architect-manager
```

Useful for inspecting a skill's constraints before invoking it, or piping the content to your clipboard for context.

---

## `skillmanager update`

Apply skill updates from a source directory. Updates pristine (unmodified) skills in place; stages modified skills for manual review.

```bash
skillmanager update --source <path>
```

`<path>` must be a directory that contains a `skills/` subdirectory — a new download or any directory structured like the SkillsLoom repository. The CLI does not manage or clone any git repository.

**Behaviour for each changed file:**
- **Pristine** (not customised since install) → updated in place automatically
- **Customised** (differs from install-time checksum) → copied to `$SKILLSLOOM_DIR/staging/` for review

After a run with staged files:
```bash
skillmanager staging ls                # list staged updates
skillmanager staging diff <name>       # diff staged vs installed
skillmanager staging accept <name>     # apply the staged version
skillmanager staging dismiss <name>    # discard staged version, keep customisation
```

---

## `skillmanager staging`

Manage new upstream versions of skills that were staged by `skillmanager update` because they had been customised.

```bash
skillmanager staging ls                  # list all staged updates
skillmanager staging diff git-manager         # diff the staged vs installed version of git-manager
skillmanager staging accept git-manager       # accept the staged version (overwrites your customisation)
skillmanager staging dismiss git-manager      # discard the staged version (keep your customisation)
```

---

## `skillmanager customize`

Interactive wizard to create environment-specific reference files and workflow skills for your installed SMEs. Safe to re-run: skips SMEs that are already customised.

```bash
skillmanager customize
```

For each active SME, the wizard asks whether you want to create a matching workflow skill with environment-specific context (e.g. project IDs, naming conventions, team standards). New workflow skills are saved to `$SKILLSLOOM_DIR/skills/<name>/` and activated automatically.

Run this after initial install to personalise the generic skills to your stack.

---

## `skillmanager lint [file]`

Check markdown quality of all SKILL.md files, or a specific file if provided.

```bash
skillmanager lint                        # check all skills
skillmanager lint skills/git-manager/SKILL.md  # check one file
```

Uses `markdownlint` when available. Falls back to basic checks (frontmatter presence, trailing whitespace, H1 heading) if not installed.

---

## `skillmanager help`

Print usage information.

```bash
skillmanager help
skillmanager --help
skillmanager -h
```
