---
name: diagram-manager
description: Diagrams — route to Mermaid code or to type/design guidance. Invoke for flows, architecture visuals, or Mermaid in markdown.
metadata:
  version: "1.0"
  disable-model-invocation: true
---
# Diagrammer (router)

**Main brain:** this file. Mermaid syntax and output: `workflows/mermaid.md`, `references/output-patterns.md`, `references/mermaid-visual-conventions.md`.

| If… | Open |
|-----|------|
| **Mermaid** / code / `.mmd` / “diagram in GitHub” | `workflows/mermaid.md` then `references/output-patterns.md` |
| **Which diagram type** (flow vs sequence vs ER) or non-Mermaid | this file — confirm format before syntax |
| Mermaid in formal docs | `references/mermaid-visual-conventions.md` |

**Default** when the user says “diagram” without naming a tool: offer **Mermaid** first unless they specify otherwise.

## Conventions (always)

- Default language: Mermaid unless the user specifies otherwise.
- Split diagrams that exceed ~15 nodes.
- Match type to the question; one concern per diagram; title every figure.
- Validate type before generating: `flowchart TD`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, C4, etc.
- Output raw Mermaid in a fenced `mermaid` block; no overlapping text, sensible subgraphs, clean line routing.
- **Type quick map:** system interactions → `sequenceDiagram`; process → `flowchart TD`; state → `stateDiagram-v2`; entities → `erDiagram`; deployment topology → C4 or `flowchart` with subgraphs.
