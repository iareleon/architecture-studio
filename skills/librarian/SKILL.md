---
name: librarian
version: 1.2.0
description: "Maintains system logs, documentation structure, and global workspace metadata. Responsible for change tracking and structural maintenance."
---

## Core Responsibilities

- **Log Management:** Maintain `raw/change-log.md` and `raw/discovery-log.md` to track all system modifications and research findings.
- **Structural Maintenance:** Ensure the workspace structure is accurately reflected in `llm/folder-structure.md` and `README.md`.
- **Governance & Scaffolding:** Initialize project layers and scaffold new change or discovery documents using internal templates. 
  - **Installation Ownership Rule:** At install, the skill owns the install. After that, the user has freedom to use the framework as per their choices. After the initial creation of a project, the `llm/install.md` is created but never changed. The Single Source of Truth (SSOT) will always be `llm/folder-structure.md`.
- **Workspace Metadata:** Update configurations, schemas, and root logs to reflect the current system architecture.

## Workflow

1. **Scaffold:** 
    - When `clarify:` is triggered: Create a `raw/discovery-log.md` entry and a `raw/discovery/` document with status `[open]`.
    - When `add:`, `update:`, or `delete:` is triggered: Create a `raw/change-log.md` entry and a `raw/changes/` document with status `[todo]`.
    - Use templates stored in `assets/templates/` (`changes.template.md`, `discovery.template.md`, etc.).
2. **Log Maintenance:**
    - **Status Updates:** Manage transitions between `[open]`, `[todo]`, `[in-progress]`, `[review]`, `[approved]`, `[rejected]`, `[reopen]`, `[closed]`, and `[done]`.
    - Ensure all logs are synchronized with the actual files in `raw/changes/` and `raw/discovery/`.
3. **Structural Update:** 
    - Perform the `tree` command (excluding `raw/changes/` and `raw/discovery/`) and update `llm/folder-structure.md`.
    - Ensure `README.md` reflects any changes to the skills directory or project layout.
4. **Maintenance:** Perform the "Single Open Row Rule" check on all managed logs and configuration files.

## Automation

- **Tree Update:** Use `tree /f` (Win) or `tree` (Unix) to refresh the folder structure, ensuring efficiency by limiting depth and excluding audit/discovery paths.
- **Relocation:** When a skill or asset is moved, update all internal links and metadata to maintain system integrity.
