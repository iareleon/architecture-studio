---
name: document-manager
description: "Technical writing — README, ADR, HLD, document audits, and structured updates. Use when the user needs a new doc from a template, a spec or ADR, a long-form HLD, a doc pass before release, or a refresh of an existing file — even if they say \"we need a doc for this\" or \"formalise this in writing.\""
metadata:
  version: "1.0"
  disable-model-invocation: true
  formerly: documenter
---
# Documenter (router)

**Main brain:** this file. Menu: `workflows/documenter-menu.md`. Analyst scaffolds: `references/analyst-templates/`.

| User intent | Load |
|-------------|------|
| General write / review / update / extend | `workflows/documenter-menu.md` |
| **Mermaid** only | `diagrammer` — `workflows/mermaid.md` |
| **Diagram type** (C4, sequence, …) | `diagrammer` — `SKILL.md` |
| New README | `workflows/documenter-readme` |
| New ADR | `workflows/documenter-adr` |
| Quality review | `workflows/documenter-audit` |
| Update / extend section | `workflows/documenter-update` / `workflows/documenter-extend` |

**File writes:** confirm **target path** with the user before writing.

## Standards (summary)

- Docs-as-Code: versioned with the code. C4 hierarchy for architecture diagrams. ADRs for structural decisions. README reflects current system.
- HLD: overview → container diagram → components → data flow → infrastructure → security → operations (detail in SME).
- No `TODO`/`TBD` in published docs; diagrams must render; define terms on first use.
- Research synthesis: as-is / to-be, personas when relevant; tie conclusions to ADRs. Use analyst templates for gaps and requirements.
- **Workflow:** collect subject first; require approval for every path; delegate diagram work to `diagrammer`.
- **Review:** structure, clarity, accuracy, discoverability, consistency with workspace standards.
