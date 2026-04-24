---
name: documenter
version: 1.0.0
description: "Handles external document generation, publishing, and formats. Use for: Integrating with external document platforms (e.g., Google Docs) for publishing."
---
## Core Responsibilities

- **Google Docs Integration:** Generate and maintain synced Google Docs versions of local markdown files (like HLDs).
- **Format Conversion:** Provide capabilities to adapt internal markdown documentation into external consumption formats (e.g., PDFs, Word docs) as future capabilities are introduced.

## Activation & Guardrails

The documenter-creator skill can be activated in two ways:
- **LLM CLI (Direct Execution):** Can be activated from within an LLM chat session contextually to directly generate or sync documents based on user requests.

## Workflow

1. **Publish to Google Docs:** When a user requests to publish a document (e.g., an HLD):
    - Execute `node scripts/publish_to_gdocs.cjs <file_path>` to generate a synced Google Doc version.
    - **Note:** Mermaid diagrams are NOT processed by this script. Ensure that a placeholder section (`[Diagram Placeholder - Insert from external source]`) is inserted in place of any Mermaid code blocks.
