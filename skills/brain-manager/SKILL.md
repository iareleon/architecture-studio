---
name: brain-manager
version: 1.1.0
description: Manages root brains (GEMINI.md) and directive propagation.
---

## Core Responsibilities

- **Governance**: Maintenance of root operational brains (global and local).
- **Directive Propagation**: Identify and execute `[/changes]` verbs in messages and logs.
- **Context Management**: Distinguish project-specific vs global directives.

## Workflows

The brain modification process follows strict auditing steps:
1. **Analyze Intent**: Determine if the change is a new directive or a clarification.
2. **Draft Modifications**: Apply `[/changes]` logic to the target brain.
3. **Validate**: Ensure changes adhere to `GEMINI.md` core directives.
4. **Approval**: Summarize impact and request explicit user confirmation.
5. **Apply**: Commit the changes to the brain file.

## Directives

### Non-Negotiable
- **95% Certainty**: Clarify scope (Global vs Local) before modification.
- **Integrity**: Never modify system mandates without multi-step verification.

### Critical
- **Silent Changes Forbidden**: Any brain modification must be logged in `raw/change-log.md` and `raw/changes/`.
- **Structural Integrity**: Ensure links between HLDs, wiki, and logs remain valid.

### High
- **Explicit Confirmation**: Summarize changes and impacts for user approval before execution.
- **Obsidian Linking**: Use `[[ ]]` for all internal document cross-references.

### Medium
- **Prioritization**: Group instructions in brains by priority (Non-negotiable to Low).

### Low
- **SME Alignment**: Audit brain rules against specialized skill instructions.
