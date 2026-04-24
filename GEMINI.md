# Architect Studio Brain

Root operational brain for Gemini CLI and local AI. Defines working principles, automation, and rules for Solutions Architect role.

## 1. Workspace Governance

The workspace is organized into four distinct functional layers to ensure modularity and traceability:

- **1. Source Layer (`raw/`)**: Immutable entry point containing source documents (BRS, PDF, Meeting Notes), and now the system's traceability records (`change-log.md`, `discovery-log.md`, `changes/`, and `discovery/`).
- **2. Memory Layer (`llm/`)**: Lean core containing `folder-structure.md` and `install.md`.
- **3. Execution Layer**: The active working area where `project/` (HLDs/Design) and `wiki/` (Living Docs) are maintained and interlinked using Obsidian `[[ ]]` links.
- **4. Audit Layer**: Traceability records now located in `raw/changes/` and `raw/discovery/`.

**Data Flow**: Source docs -> Memory Ingestion -> Execution (Project/Wiki) -> Audit Logging -> Memory Update.

## 2. Workflows

### Discovery
Trigger: `clarify: <question>`
1. **Queue**: Librarian creates `[open]` entry in `discovery-log.md`.
2. **Scaffold**: Librarian creates `discovery/YYYY-MM-DD-HH24-MM-name.md` with status `[open]`.
3. **Research**: Researcher performs synthesis, updates log to `[in-progress]`, and sets final status to `[review]`.
4. **Approval**: User reviews findings to set status to `[closed]` or `[reopen]` if further work is needed.

### Change
Trigger: `add:`, `update:`, `delete:`, or `question:`
1. **Log**: Librarian adds entry to `change-log.md` with status `[todo]`.
2. **Plan**: Librarian scaffolds `changes/YYYY-MM-DD-HH24-MM-name.md` and sets status to `[review]`.
3. **Execution**: Upon user approval (`[approved]`), changes are applied, log status is set to `[in-progress]`, and finally `[done]`.

## Statuses

### Discovery
- **`[open]`**: New research inquiry identified.
- **`[reopen]`**: User requires additional research or clarification.
- **`[closed]`**: Research finalized and findings accepted.

### Changes
- **`[todo]`**: Change identified, awaiting planning.
- **`[approved]`**: Plan reviewed and approved for execution.
- **`[done]`**: Change fully implemented and verified.
- **`[rejected]`**: Change request cancelled or dismissed.

### Common
- **`[in-progress]`**: Active work (Research or Implementation) is occurring.
- **`[review]`**: Ready for user feedback or approval.

## 4. Directives

### Non-Negotiable
- **Single File Focus**: When requested to read a single file, ONLY read and focus on that specific file. Do NOT read or analyze any other resources unless explicitly instructed.
- **Precision Mandate**: The LLM must not accept vague instructions. If a prompt or request is imprecise, the LLM MUST stop and ask clarifying questions to ensure a deterministic and accurate execution.
- **State Check**: Consult `llm/folder-structure.md` before taking any action.
- **95% Certainty Rule**: Stop and ask if unsure. Do not guess user intent or system state.
- **Zero Hallucination**: Rely only on context, research, or explicit instructions.

### Critical
- **Silent Changes Forbidden**: Every modification MUST be logged.
- **File Naming**: ALL files in the workspace MUST follow the format `YYYY-MM-DD-HH24-MM-{filename}.md` (24HH notation, SAST/GMT+2). This applies to audit, discovery, wiki, and project documents.
- **Structural Propagation**: Ensure `llm/folder-structure.md` and `README.md` reflect all structural changes.
- **Safety**: Verify with user before any deletion of content or files.

### High
- **Audit Reporting**: All audit skills MUST write their generated reports to the `raw/reports/` directory using the standard 24HH file naming convention (`YYYY-MM-DD-HH24-MM-audit-name.md`).
- **Initial Read**: Start every session by reading `llm/folder-structure.md`.
- **Directive Monitor**: Execute immediately upon detecting `[/changes]` verbs.
- **Global Linking**: Maintain link integrity using Obsidian-style `[[ ]]` links.
- **Plan First**: Always enter Plan Mode and get approval before file modifications.
- **Cost Efficiency**: Content in the `/raw/` directory MUST always be excluded from implicit reads. This entire layer is for explicit reads only, initiated by specific user queries or required for direct task validation.

### Medium
- **SME Delegation**: Use specialized skills (`researcher`, `librarian`, `auditor`, `system-analyst`, etc.) for domain tasks.
- **Tech Agnostic**: Remain technology agnostic unless a specific stack is explicitly requested.

### Low
- **Audit Outcomes**: Log the final outcome of all task executions in the appropriate `/changes/` record.
