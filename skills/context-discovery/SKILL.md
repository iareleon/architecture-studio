---
name: context-discovery
version: 1.0.0
description: Architectural discovery for projects starting without a BRD.
---
## Core Responsibilities
- **Zero-BRD Bootstrapping:** Conduct interactive discovery sessions to extract:
    - **User Personas:** Who is the end user?
    - **Value Prop:** What is the "Job to be Done"?
    - **Data Entities:** What are the nouns?
- **Implicit Requirement Mapping:** Infer NFRs based on the described scale (e.g., "Public web app" implies High Availability/DDoS protection).
- **Seed-Brain Generation:** Create the first draft of `llm-memory/discovery-log.md` using the `discovery-log.template.md` provided by the librarian skill and the initial project overview documents.

## Workflow
1. **Interview:** Prompt the user for a high-level "Elevator Pitch" of the system.
2. **Extrapolate:** Generate a "System Context Diagram" (Mermaid) based on the pitch.
3. **Iterate:** Ask 3-5 high-signal questions to narrow down the architecture (e.g., "Batch vs Real-time?").
4. **Settle:** Output a "Project Kickstart" document that serves as the temporary BRS.
