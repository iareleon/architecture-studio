---
name: auditor
version: 1.0.0
description: "Unified auditing skill for structural integrity, performance monitoring, prompt optimization, and compliance verification."
---

## Personas

This skill operates through specialized auditing personas:
- **[[assets/personas/structural.md|Structural Auditor]]**: Enforces workspace governance and naming conventions.
- **[[assets/personas/performance.md|Performance Auditor]]**: Monitors context efficiency and LLM performance.
- **[[assets/personas/prompt.md|Prompt Auditor]]**: Identifies redundancy and codifies recurring patterns.
- **[[assets/personas/compliance.md|Compliance Auditor]]**: Validates formatting rules, skill integrity, and link consistency.

## Core Responsibilities

- **Structural Integrity:** Ensure the workspace adheres to the `GEMINI.md` governance rules and folder structure.
- **Performance Monitoring:** Analyze context usage, prompt density, and token efficiency.
- **Prompt Optimization:** Audit user prompts for redundancy, duplication, and optimization opportunities.
- **Compliance & Validation:** Enforce formatting standards (Single Open Row Rule) and validate skill definitions.
- **Continuous Learning:** Scan recent logs for recurring patterns to codify into new skills or instructions.

## Workflow

1. **Trigger:** Audit initiated by user, scheduled framework check, or autonomous detection of recurring patterns.
2. **Selection:** Always ask the user which audit must be done and by which persona before proceeding.
3. **Analysis:** Evaluate the target against the rules defined in the active **Persona**.
4. **Synthesis:** Generate a detailed report using the `audit-report.template.md`. Save to `raw/reports/` using the standard `YYYY-MM-DD-HH24-MM-audit-report.md` format.
5. **Actionable Output:** Propose specific `[/changes]` or `clarify:` items to resolve identified gaps.
6. **Codification:** If a pattern is identified, log it as an improvement (new skill, core instruction, or local instruction).

## Automation & Guardrails

- **Librarian Integration:** Can be used by the `librarian` to generate the `audit-fix-plan.md`.
- **Validation Script:** Run `node scripts/validate_skill.cjs <skill_name>` to ensure skill compliance.
- **Improvement Logging:** Use `node scripts/log_improvement.cjs "<category>" "<description>"` to record gaps.
