---
name: ignore-manager
version: 1.0.0
description: Create and manage .ignore files for the project.
---
## Core Responsibilities
- **Ignore File Creation:** Prompt the user to determine which type of ignore file is needed (e.g., `.gitignore`, `.geminiignore`, `.dockerignore`).
- **Template Application:** Use standard templates to bootstrap ignore files based on the project's technology stack.
- **Customization:** Add custom ignore patterns based on specific project requirements (e.g., ignoring `.obsidian/` or `llm/changes/`).

## Workflow
1. **Prompt:** Ask the user which `.ignore` file must be created or updated.
2. **Contextual Analysis:** Identify common patterns for the current tech stack (e.g., `node_modules`, `__pycache__`, `.env`).
3. **Write:** Create or update the specific `.ignore` file in the project root.
4. **Verify:** Confirm the file exists and contains the expected patterns.
