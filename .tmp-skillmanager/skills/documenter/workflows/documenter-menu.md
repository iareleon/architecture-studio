# Document

Presents a template and operation menu, collects the document subject, and routes to the appropriate subflow. All file writes require explicit user approval of the target location before execution.

## Workflow

### 1. Collect Subject

Ask the user what the document is about:

```
What is the document subject or purpose?
(e.g. "a Node.js REST API for managing orders", "the checkout service architecture")
```

Hold the subject as context for the activated subflow.

### 2. Select Operation

```
What would you like to do?

  1. Write a new document
  2. Review an existing document
  3. Update an existing document
  4. Add content to an existing document

Enter 1–4:
```

### 3a. New Document — Select Template

If the user selected 1:

```
Select a document template:

  1. Git README.md        — discoverable project readme optimised for GitHub/GitLab
  2. Mermaid diagram      — architecture, flow, sequence, or state diagram
  3. ADR                  — Architecture Decision Record
  4. Other                — describe the document type you need

Enter 1–4:
```

- `1` → load `workflows/documenter-readme.md`, pass the subject.
- `2` → activate `diagram`, pass the subject.
- `3` → load `workflows/documenter-adr.md`, pass the subject.
- `4` → ask: "Describe the document type (e.g. runbook, API reference, onboarding guide)." Then load `workflows/documenter-readme.md` with a generic document mode, or inform the user that this template is not yet available and suggest the closest match.

### 3b. Existing Document Operations

If the user selected 2 → load `workflows/documenter-audit.md`.
If the user selected 3 → load `workflows/documenter-update.md`.
If the user selected 4 → load `workflows/documenter-extend.md`.

For operations 2–4, ask: `Path to the existing document:` before loading the subflow.

### 4. Post-Operation

After the subflow completes, ask:

```
Anything else? (select another operation or "done")
```

Return to Step 2 on any new request. Exit on "done".

## Guidelines

- **Subject carries through** — always pass the collected subject to the subflow so it does not ask again.
- **Location approval is mandatory** — every subflow that writes a file must confirm the target path with the user before writing.
- **diagram is external** — it is an existing skill; activate it directly for diagram requests, do not replicate its logic here.

## Subflows

| File | Load when |
|---|---|
| `workflows/documenter-adr.md` | User wants to create an Architecture Decision Record |
| `workflows/documenter-readme.md` | User wants to draft a Git README.md |
| `workflows/documenter-audit.md` | User wants to review an existing document |
| `workflows/documenter-update.md` | User wants to update sections of an existing document |
| `workflows/documenter-extend.md` | User wants to add content to an existing document |

## Related context

- Technical writing baselines: this skill’s `SKILL.md`
- **Diagram** work: `diagram` skill — Mermaid in `workflows/mermaid.md`; type choice in `diagrammer` `SKILL.md`

## HLD and structured design templates

For large HLDs, use the scaffold library in `references/hld-templates/`. Start from `references/hld-templates/hld.template.md` and pull sections (macro overview, NFRs, risks, glossary, etc.) as needed.

## External publishing

When syncing to external systems (e.g. Google Docs, PDF), confirm how diagrams are handled — many exporters omit Mermaid; use explicit placeholders and manual follow-up if required.

## Bootstrapping context from source documents

When ingesting BRS/PRD/HLD material to refine project context, extract: commercial guardrails, tech stack, domain terminology, and scope boundaries. Resolve conflicts between local and global rules before writing shared guidance.

## References

- `references/hld-templates/hld.template.md` — master HLD scaffold (see directory for section templates)
