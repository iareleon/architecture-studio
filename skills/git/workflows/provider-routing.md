# Provider routing

Routes **local** `git` + hosting operations by remote.

- **GitHub** remote → follow `github-platform.md` and `references/github-operations.md`.
- **GitLab** remote → follow `gitlab-platform.md` and `references/gitlab-operations.md`.
- If unclear, ask: GitHub (1) or GitLab (2), then open the matching platform workflow file.

All execution uses dry-run → confirm, as in each platform file. The parent skill name is `git` (one folder; two platform procedures).

## Detect provider

```bash
git remote get-url origin 2>/dev/null
```

- `github.com` in URL → GitHub.
- `gitlab.com` or known self-hosted GitLab host → GitLab.
- No / ambiguous → prompt 1/2, then open the right **platform** subflow above.

## Guidelines

- Auto-detect before asking.
- Do not hand off to a platform subflow until the provider is known.
- One provider per session unless the user asks to switch.
