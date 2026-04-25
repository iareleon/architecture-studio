# Tests

Automated tests for the `skillmanager` CLI using [pytest](https://docs.pytest.org/).

---

## Install dependencies

```bash
pip install pytest
```

---

## Run the tests

From the project root:

```bash
pytest tests/test_skillforge.py -v
```

---

## What is tested

| Test | Description |
|---|---|
| `version` | Prints a version string |
| `help` | Exits 0 and includes usage information |
| `help <unknown>` | Exits non-zero for unknown commands |
| `no args` | Prints a hint and exits non-zero |
| `ls` | Lists skills from the fixture directory |
| `audit` / `sync` | Creates or removes symlinks from `metadata.status` |
| `audit (violation)` | Detects and fixes a missing symlink for active skills |
| `deactivated` in SKILL | Audit removes production symlinks |
| `staging` / `review` in SKILL | Audit adjusts staging vs production links |
| `show <unknown>` | Exits non-zero for unknown skills |
| `audit (clean)` | Passes with no violations |
| `lint` | Passes on a valid SKILL.md |
| `doctor` | Exits 0 and shows environment information |
| `config` | Prints config file contents |
| `unknown command` | Exits non-zero with a helpful message |

---

## Fixtures

`tests/fixtures/` contains minimal skill directories used in tests. These are isolated from your real skill install — tests run against a temporary directory (`tmp_path`) and are cleaned up after each test.

Do not activate fixture skills in a real session. They are for testing only.

---

## Philosophy

These tests verify CLI behaviour, not AI output. You cannot reliably test what the AI will say — but you can test that:
- `metadata.status` maps to the right symlinks after `audit`
- Symlinks are created and removed
- Violations are detected and fixed
- The CLI fails gracefully on bad input

---

## LLM eval tests

`tests/run_evals.sh` runs integration tests that actually call the Anthropic API and check structural properties of the model's response (keyword presence, format) rather than exact wording. These are inherently non-deterministic.

### Prerequisites

```bash
export ANTHROPIC_API_KEY=sk-...
```

If `ANTHROPIC_API_KEY` is not set, the runner exits 0 with a `[SKIP]` message — it never blocks CI without a key.

### Run all evals

```bash
ANTHROPIC_API_KEY=sk-... bash tests/run_evals.sh
```

### Run evals for one skill

```bash
ANTHROPIC_API_KEY=sk-... bash tests/run_evals.sh tests/evals/git/
```

### Run a single eval

```bash
ANTHROPIC_API_KEY=sk-... bash tests/run_evals.sh tests/evals/git/plan-mode-gate.eval.md
```

---

## Eval file format

Eval files live in `tests/evals/<skill-name>/` and are named `<scenario>.eval.md`.

```markdown
---
skill: git
description: "One-line description of what behaviour is being tested"
model: claude-haiku-4-5-20251001
max_tokens: 512
---

## Prompt

The user message sent to the API.

## Assertions

- contains: "keyword"
- not_contains: "bad phrase"
- contains_any: "word1|word2|word3"
- matches_regex: "pattern"
- min_words: 30
- min_length: 100
```

### Frontmatter fields

| Field | Required | Default | Description |
|---|---|---|---|
| `skill` | yes | — | Skill directory name (e.g. `git`) |
| `description` | yes | — | What behaviour is being tested |
| `model` | no | `claude-haiku-4-5-20251001` | Model ID to use (haiku keeps cost low) |
| `max_tokens` | no | `512` | Max tokens in the response |
| `memory_file` | no | (none) | Optional extra path under the skill dir (e.g. `persona/local.md`); appended when the file exists |

### Assertion types

| Type | Example | Meaning |
|---|---|---|
| `contains` | `contains: "plan"` | Response must contain this string (case-insensitive) |
| `not_contains` | `not_contains: "sure"` | Response must NOT contain this string |
| `contains_any` | `contains_any: "a\|b\|c"` | At least one alternative must appear (pipe-separated) |
| `matches_regex` | `matches_regex: "feat\|fix"` | Response must match this extended regex |
| `min_words` | `min_words: 30` | Response must be at least this many words |
| `min_length` | `min_length: 100` | Response must be at least this many characters |

### Writing good assertions

- Test behavioural signals, not exact phrasing — LLM output varies across calls and model versions
- Use `contains_any` with pipe-separated alternatives rather than a single keyword where possible
- Pair a positive assertion (`contains`) with a negative one (`not_contains`) for stronger coverage
- Keep `min_words` low enough to pass even for concise responses

---

## Existing evals

| Eval | Skill | Tests |
|---|---|---|
| `plan-mode-gate` | `git` | Plan mode is enforced before executing git commands |
| `no-force-push-to-main` | `git` | Force-push to main is blocked |
| `hardcoded-secret-flag` | `security` | Hardcoded credentials are flagged immediately |
| `domain-layer-boundary` | `architect` | Infrastructure in the domain layer is rejected |
