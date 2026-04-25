# Design Import Workflow

Convert a raw Claude design artifact from `raw/` into a structured product spec.

## Input

- `raw/{raw-file}.md` — a design artifact produced by a Claude design session.
  Typically contains component descriptions, UX flows, data models, or API sketches.

## Steps

1. Read `raw/{raw-file}.md` fully.
2. Identify the design type from content:
   - **UX flow** — user journeys, screen descriptions, interaction patterns
   - **Data model** — entities, relationships, field definitions
   - **API sketch** — endpoint descriptions, request/response shapes
   - **Component spec** — UI component breakdown, props, states
3. Produce a structured spec at `research/active/{idea-slug}-design-spec.md`:

```markdown
---
type: design-spec
idea: {idea-slug}
design-type: {ux-flow | data-model | api-sketch | component-spec}
status: researched
date: YYYY-MM-DD
source: raw/{raw-file}.md
---

# Design Spec — {idea title}

## Summary
{2–3 sentences on what this design covers}

## {Section per design-type}
{structured content extracted from the artifact}

## Open Questions
{any ambiguities identified during import}
```

4. Set `status: researched`.
5. Append to `_os/log.md`: `## [date] design-import | {idea-slug}`.
6. Report: `Design spec complete → research/active/{idea-slug}-design-spec.md`.
