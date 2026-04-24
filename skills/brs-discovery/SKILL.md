---
name: brs-discovery
version: 1.0.0
description: Ingests project source documents (BRS/PRD/HLD) to bootstrap the 'Local Brain' (GEMINI.md).
---
## Core Responsibilities
- **Semantic Extraction:** Read raw project documents (e.g., `business-clarifications.md`, `BRS.pdf`) and identify:
    - **Commercial Guardrails:** What is the "Source of Truth" for finance?
    - **Tech Stack:** What tools are in play (Cloud, ERP, CRM, etc.)?
    - **Terminology:** What are the domain-specific nouns (e.g., "Campaign," "Wallet," "Line Item")?
- **Scope Separation:** Explicitly define the separation between Local context (project specifics like "Cloud Provider", "Database Type") and Global context (enterprise-wide guardrails, methodology, or formatting rules).
- **Brain Bootstrapping:** Generate or update the target `GEMINI.md` (local or global) with directives that align skills to these facts.
- **Memory Initialization:** Create the `llm/` structure (using `discovery-log.template.md` and `folder-structure.template.md` provided by the librarian skill for scaffolding) if missing.

## Workflow
1. **Scope:** Determine the target `--scope` (local or global) for the extraction.
2. **Ingest:** Use `read_file` or `grep_search` to scan the appropriate root or documents for source-of-truth details.
3. **Analyze:** Cross-reference found data against the "Standard Engagement Protocol."
4. **Program:** Locate the correct `GEMINI.md` file based on the determined scope (local project root or global config folder). Write the findings into the `GEMINI.md` under a `# Project Context` or equivalent section. 
    - *Conflict Resolution Rule:* If a local context rule contradicts an existing global rule, flag it for the user before writing to the local `GEMINI.md`.
5. **Validate:** Confirm the updated instructions are active.
6. **Reload Memory:** If any change is made to the global/local `GEMINI.md` files, session memory must be reloaded.
