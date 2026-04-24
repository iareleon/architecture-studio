---
name: skill-creator
version: 1.1.0
description: Skill creation and extension guide.
---

## Workflows

The skill creation process follows a standard sequence to ensure compliance:
1. **Analyze Requirements**: Determine the specific expert role needed.
2. **Scaffold Skill**: Read `skills/skill-creator/assets/templates/SKILL.template.md`.
3. **Draft SKILL.md**: Define workflows and directives using text-rich descriptions.
4. **Update README.md**: Add the new skill to the Skills Directory table.
5. **Validation**: Use the `auditor` skill (Compliance persona) to package and validate the new skill.

## Directives

### Non-Negotiable
- **Template Mandatory**: Bootstrap using `skills/skill-creator/assets/templates/SKILL.template.md`.
- **Single Responsibility**: Exactly one primary capability per skill. No omni-skills.
- **Asset Standardisation**: Sub-assets MUST use standardized naming:
    - Personas MUST be stored in `assets/personas/`.
    - Templates MUST be stored in `assets/templates/`.
- **Architectural Alignment**: Follow `GEMINI.md` (Text-rich standards, file naming, Obsidian links).

### Critical
- **Validation Mandate**: Skill incomplete until passed by `auditor` (Compliance persona) and packaged.
- **No type Property**: Frontmatter must not contain logical-value-free `type` property.

### High
- **Safety First**: Prefer declarative instructions and native CLI tools over bash scripts.
- **Timestamp Accuracy**: ALL files in the workspace (including those in `raw/changes/` or `raw/discovery/`) must follow the `YYYY-MM-DD-HH24-MM-{filename}.md` format (24HH, SAST).

### Medium
- **Contextual Constraint**: Keep skills focused on specific procedural or domain requirements.

### Low
- **Auto-Detection**: No manual reload required; system detects new skill files automatically.
