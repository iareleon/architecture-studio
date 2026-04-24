# 2026-04-22-07-55-script-migration-python

**Status: [closed]**

## Objective

Clarify if all scripts in the Architecture Studio workspace can be migrated from their current mixed state (Node.js and Python) to a unified Python-based automation stack.

## Findings

- **Current Script Landscape:** The workspace currently employs Node.js (`.cjs`) for auditing and Google Docs synchronization (4 scripts) and Python (`.py`) for meeting note formatting (1 script).
- **Governance Alignment:**
    - The `GEMINI.md` file mandates a "Tech Agnostic" approach, meaning there is no hard restriction preventing a migration to Python.
    - The `README.md` (specifically for New Applications) lists Python or Go as the default for CLI tools.
- **Technical Portability:**
    - **Auditor Scripts:** `audit_structure.cjs`, `validate_skill.cjs`, and `log_improvement.cjs` are primarily file system and regex-based operations. These are highly compatible with Python's standard library (`os`, `pathlib`, `json`, `re`).
    - **Documenter Script:** `publish_to_gdocs.cjs` relies on `googleapis` and `marked`. This can be ported using `google-api-python-client` and `markdown2` or `mistune`, though it would require transitioning from `package.json` to a `requirements.txt` or `pyproject.toml` for dependency management.
- **Strategic Value:** Unifying the automation layer under Python simplifies the environment setup for users, as it reduces the need to manage both Node.js and Python runtimes for workspace maintenance.

## Architectural Recommendations

- **Unified Stack:** Standardize all workspace CLI/Automation scripts to Python to align with existing project defaults for CLIs.
- **Dependency Management:** If migration proceeds, implement a standard Python dependency management pattern (e.g., skill-specific `requirements.txt`) to replace `package.json`.
- **Command Update:** Ensure all `SKILL.md` files are updated to call `python` instead of `node` for automated workflows.

## Next Steps

- Identify a pilot script (e.g., `audit_structure.cjs`) for conversion to Python.
- Create a corresponding `[/changes]` request to execute the migration once the user decides to proceed.
