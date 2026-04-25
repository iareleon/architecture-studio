# Passage Research Workflow

Research a Bible passage cluster (e.g. `genesis-1-3`) and produce a structured study note.

## Input

- `{cluster-slug}` — a passage range, e.g. `genesis-1-3`, `john-3-16-21`.
  Granularity: narrative clusters, not atomic per-chapter (see ADR-02 in SKILL.md).

## Steps

1. Identify the passage boundaries and canonical reference.
2. Read the raw passage from any available source or user-provided text.
3. Extract and structure:
   - **Context** — historical, cultural, and canonical context
   - **Key themes** — recurring motifs, theological concepts
   - **People** — named individuals mentioned, their roles
   - **Cross-references** — other passages that echo or extend the same theme
   - **Interpretive notes** — significant scholarly positions or translation variants
   - **Personal reflection prompts** — 3–5 open questions for study

4. Output `research/active/{cluster-slug}.md`:

```markdown
---
type: passage
cluster: {cluster-slug}
reference: {Book Chapter:Verse–Chapter:Verse}
status: researched
date: YYYY-MM-DD
themes: []
people: []
---

# {Reference}

## Context
{historical and canonical context}

## Key Themes
{themes with brief notes}

## People
{named individuals and their roles}

## Cross-References
{related passages}

## Interpretive Notes
{significant notes}

## Reflection Prompts
1. ...
2. ...
3. ...
```

5. Append to `_os/log.md`: `## [date] ingest | {cluster-slug}`.
6. Report: `Research complete → research/active/{cluster-slug}.md`.
