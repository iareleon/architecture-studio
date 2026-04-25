# Mermaid visual conventions (maintenance and governance)

Use when diagrams must stay consistent across HLDs, wikis, and runbooks.

- Prefer rectangles over circle/database shapes unless the diagram type requires otherwise.
- Use colour deliberately: differentiate phases or component classes; keep a legend for multi-colour diagrams.
- Connectors should carry short labels explaining flow or data.
- Enable autonumbering for sequence and process flows where supported.
- Integration-style links (APIs, buses) are visually distinct (e.g. dashed) from synchronous control flow.
- Multi-line node text: keep a single `<br>` between title and detail when splitting lines.
- After edits, confirm the diagram renders in the target Markdown viewer.
