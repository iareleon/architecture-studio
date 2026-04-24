---
name: dependency-manager
version: 1.0.0
description: Helps non-technical users install and manage software dependencies like Node.js, Python, and Git using automated package managers.
---
## Core Responsibilities
- **Requirement Detection:** Scan the project for configuration files (e.g., `package.json`, `.nvmrc`, `requirements.txt`, `Gemfile`, `go.mod`) to identify necessary runtimes and versions.
- **Automated Installation Guidance:** Provide clear, copy-pasteable commands for system package managers (primarily `winget` for Windows) to install missing dependencies.
- **Environment Verification:** Run version check commands to ensure that the installed software is correctly configured in the system PATH and matches required versions.

## Workflow
1. **Diagnosis:** Run a system check to identify existing tools and their versions. Compare these against detected project requirements.
2. **Package Manager Check:** Verify if `winget` (Windows Package Manager) is available and functioning.
3. **Prescriptive Guidance:**
   - If a tool is missing, provide the specific `winget install` command.
   - Example: `winget install OpenJS.NodeJS.LTS` for Node.js.
   - Example: `winget install Python.Python.3.12` for Python.
4. **Manual Fallback:** If `winget` is unavailable, provide direct official download links and simple installation instructions.
5. **Verification:** Instruct the user to run `node -v`, `python --version`, etc., to confirm success.
6. **Troubleshooting:** Provide basic tips for common issues like "command not found" (PATH issues).
