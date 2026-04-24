---
name: diagram-manager
version: 1.0.0
description: Specialized skill for creating and maintaining visual documentation, starting with Mermaid.
---

## Core Responsibilities

- **Visual Documentation:** Generate high-quality, standardized diagrams to represent system architectures, workflows, and data models.
- **Consistency Governance:** Ensure all diagrams adhere to the established "Architect Studio" visual standards.
- **Diagram Maintenance:** Update existing diagrams across the workspace (Brains, HLDs, Wiki) to reflect structural changes.

## Diagramming Standards (Sub-Skill: Mermaid)

All Mermaid diagrams MUST adhere to these strict directives:

- **Component Shape:** Never use circle or database components; only use rectangles.
- **Color Coding:** 
    - Use colors to differentiate macro document phases or processes.
    - Components in detailed design documents must be colored differently based on type (e.g., actors, application components, data objects).
- **Contextual Connectors:** All connectors must provide short contextual explanations of the interaction or data flow.
- **Auto-numbering:** Always enable auto-numbering for sequence diagrams and process flows.
- **Integration Visuals:** Integration connectors (e.g., API calls, message bus) must always be dashed.
- **Multi-line Text:** Phases/Process Components must only contain a `<br>` between "Phase/Process # Description" and "Phase/Process Detail".
- **Reference Examples:** Consult `examples\**` to see how these notations are applied for Architectural Design Documents (ADDs).

## Workflow

1. **Analyze Intent:** Determine the goal of the diagram (e.g., "Visualize the authentication flow").
2. **Select Type:** Choose the appropriate Mermaid diagram type (e.g., `graph TD` for flowcharts, `sequenceDiagram` for interactions).
3. **Draft:** Generate the Mermaid code following the standards above.
4. **Integrate:** Insert the diagram into the target Markdown file (`GEMINI.md`, HLD, Wiki).
5. **Verify:** Ensure the diagram renders correctly and accurately represents the subject matter.
