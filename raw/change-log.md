# Change Log: System & Architecture Modifications

This document serves as an index of all architectural, structural, and significant codebase modifications applied to the project. Detailed execution plans and impacts are documented in the `raw/changes/` directory.

**Full Project Audit and Log Reset**
	- **Date-Time :** 2026-04-21-22:15
	- **Phase Impacted :** Governance and Workspace Integrity
	- **Status :** [done]
	- **Question :** Perform a full audit of the project structure and logs following cleanup.
	- **Reference:** [[raw/changes/2026-04-21-22-15-full-project-audit-and-log-reset.md]]

**Implement Google Docs Sync Script**
	- **Date-Time :** 2026-04-22-07-30
	- **Phase Impacted :** Documentation and External Publishing
	- **Status :** [done]
	- **Question :** Implement missing publish_to_gdocs.cjs script for the documenter skill.
	- **Reference:** [[raw/changes/2026-04-22-07-30-implement-gdocs-sync.md]]

**Rename Decision Log Template**
	- **Date-Time :** 2026-04-22-10-35
	- **Phase Impacted :** Governance and Templates
	- **Status :** [done]
	- **Question :** Rename the decision log template to decision.log and remove date-time requirement.
	- **Reference:** [[raw/changes/2026-04-22-10-35-rename-decision-log-template.md]]

**Workspace Sync and Structural Audit**
	- **Date-Time :** 2026-04-22-11-20
	- **Phase Impacted :** Workspace Integrity & Governance
	- **Status :** [done]
	- **Question :** Audit the project and apply manual updates made by the user.
	- **Reference:** [[raw/changes/2026-04-22-11-20-workspace-sync-and-audit.md]]

**Cost Efficiency Directive & Workspace Cleanup**
	- **Date-Time :** 2026-04-22-11-30
	- **Phase Impacted :** Governance & Context Optimization
	- **Status :** [done]
	- **Question :** Update GEMINI.md with cost efficiency directive and clarify script redundancy.
	- **Reference:** [[raw/changes/2026-04-22-11-30-update-efficiency-directive.md]]

**Enable Git-Manager CLI Capability**
	- **Date-Time :** 2026-04-22-12-15
	- **Phase Impacted :** Governance & Skill Evolution
	- **Status :** [done]
	- **Question :** Enable git-manager to be used from a terminal CLI with LLM-generated commit summaries.
	- **Reference:** [[raw/changes/2026-04-22-12-15-enable-git-manager-cli.md]]

**Project Restructuring: Lean LLM & Raw Traceability**
	- **Date-Time :** 2026-04-22-12-30
	- **Phase Impacted :** Governance & Workspace Optimization
	- **Status :** [done]
	- **Question :** Restructure the workspace to make /llm/ lean and move traceability logs to /raw/.
	- **Reference:** [[raw/changes/2026-04-22-12-30-restructure-llm-and-raw.md]]

**Expand /raw/ Ringfence for Cost Efficiency**
	- **Date-Time :** 2026-04-22-13-15
	- **Phase Impacted :** Governance & Context Optimization
	- **Status :** [done]
	- **Question :** Change the global explicit read rule to /raw, so that we can ringfence that entire raw layer.
	- **Reference:** [[raw/changes/2026-04-22-13-15-expand-raw-ringfence.md]]

**Implement 'as' Alias System for CLI-Style Commands**
	- **Date-Time :** 2026-04-22-13-30
	- **Phase Impacted :** Governance & CLI UX Evolution
	- **Status :** [done]
	- **Question :** Create the ability to use aliases to execute terminal cli commands, i.e. as git -add, as librarian --audit.
	- **Reference:** [[raw/changes/2026-04-22-13-30-implement-as-alias-system.md]]

**Add Audit Selection Rule to Auditor Skill**
	- **Date-Time :** 2026-04-22-13-48
	- **Phase Impacted :** Governance & Auditing
	- **Status :** [done]
	- **Question :** Add a new audit rule, always ask the user which audit must be done and by which persona.
	- **Reference:** [[raw/changes/2026-04-22-13-48-add-audit-selection-rule.md]]
