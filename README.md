
# Architecture Studio

A high-performance workspace for Solutions Architects and AI SMEs.

| Topic Name | Values/Description |
| :--- | :--- |
| **Architectural Design** | Event-driven, edge architecture, and single responsibility focus. |
| **AI Personas** | Expert guidance via specialized skills (`activate_skill`). |
| **Governance** | Mandatory planning and terminal-based audit guardrails. |
| **Traceability** | Immutable change logs and discovery archives. |

## Workspace Playbook

### 1. Engaging the AI (LLM CLI)

| Topic Name | Values/Description |
| :--- | :--- |
| **Personas** | The AI operates through specialized skills (personas). Use the `activate_skill` tool to load expert guidance for specific tasks. |
| **Planning** | The AI will always enter **Plan Mode** before making changes. Review and approve the `.md` plan file before proceeding. |
| **Traceability** | Every modification is logged in the `raw/changes/` directory and indexed in `raw/change-log.md`. |

### 2. Guardrails & Governance (Terminal CLI)

| Topic Name | Values/Description |
| :--- | :--- |
| **Structural Integrity** | The workspace employs terminal-based scripts to maintain structural integrity and validate skill evolution. |
| **Hard Guardrails** | Scripts act as hard guardrails before AI-driven execution. |
| **Naming Convention** | All files MUST follow the `YYYY-MM-DD-HH24-MM-{filename}.md` format (24HH) for global traceability. |

### 3. Workflows

#### Change Workflow
The change workflow ensures that all modifications are deliberate and documented:
1. **Trigger**: User issues a directive prefix (`add:`, `update:`, `delete:`).
2. **Log & Scaffold**: `librarian` creates a log entry and a change document (Status: `[todo]`).
3. **Review**: User reviews the implementation plan.
4. **Execute**: Changes are applied and status is set to `[done]`.

#### Discovery Workflow
The discovery workflow manages research and requirements gathering:
1. **Trigger**: A research task is identified via the `clarify:` verb.
2. **Log & Scaffold**: `librarian` creates a discovery log entry and a research file (Status: `[open]`).
3. **Research**: `researcher` investigates and updates the file (Status: `[review]`).
4. **Review**: User approves findings (Status: `[closed]`) or identifies further changes.

### 4. Skill & Persona Activation

Specialized expertise is activated through a two-tier process: **Skill Activation** and **Persona Activation**.

#### Skill Activation (`activate_skill`)
Skills are loaded using the `activate_skill` tool. This tool imports the core instructions and workflows defined in a skill's `SKILL.md` file.
*   **Trigger:** When a task requires specialized knowledge (e.g., auditing, research, or coding).
*   **Mechanism:** Calling `activate_skill(name: "skill-name")` injects expert guidance into the session.

#### Persona Activation (Contextual Specialization)
Personas are granular specializations located in `assets/personas/` within a skill directory. 
*   **Mechanism:** Once a skill is active, the AI selects the appropriate persona `.md` file based on the project context.
*   **Example:** Activating `dev-engineer` first, then loading the `react.md` persona when React code is detected.

### 5. Monitoring Active Skills & Personas

To maintain visibility into the current session state, you can monitor active expertise through several methods:

*   **Direct Inquiry:** Ask the AI directly: *"Which skills are currently activated?"* or use the status verb: `status: active skills`.
*   **Session Logs:** Active skills are wrapped in `<activated_skill>` tags within the conversation history. The AI will also state when it is loading a specific persona from `assets/personas/`.
*   **Performance Audit:** Use the `auditor` skill with the **Performance Auditor** persona to generate a report in `raw/reports/`. This report analyzes context usage and identifies which specialized instructions are currently active.

## Alias System: 'as <skill> <args>'

To enable a natural CLI experience, you can execute skill-specific commands using short aliases.

### 1. How it works
The system uses a universal dispatcher defined in `.gemini/commands/as.toml`. It maps aliases like `git`, `librarian`, and `audit` to their respective expert skills.

### 2. Setup (One-time)
To use `as` directly in your terminal without the `/` prefix, add the following function to your PowerShell profile:

1. Open your profile in an editor:
   ```powershell
   notepad $PROFILE
   ```
2. Append this function:
   ```powershell
   function as { gemini "/as $args" }
   ```
3. Reload your profile:
   ```powershell
   . $PROFILE
   ```

### 3. Usage Examples
- `as git --all`: Activate `git-manager` and perform a full repo check.
- `as librarian --audit`: Activate `librarian` to audit the workspace.
- `as audit --structural`: Activate the `auditor` with the structural persona.

---

## Skills Directory

The workspace utilizes specialized AI personas (Skills) to provide expert guidance and maintain system integrity.

#### `architect-integrator`
| Property | Value |
| :--- | :--- |
| **Description** | Cross-vertical architectural synthesis and SME validation. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `architect-orchestrator`
| Property | Value |
| :--- | :--- |
| **Description** | Orchestrates A2A engagement across Cyber, DevOps, and Data SMEs. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `brain-manager`
| Property | Value |
| :--- | :--- |
| **Description** | Governance of global vs local local instructions (GEMINI.md). |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `brs-discovery`
| Property | Value |
| :--- | :--- |
| **Description** | Ingests project source documents (BRS/PRD/HLD) to bootstrap the 'Local Brain'. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `context-discovery`
| Property | Value |
| :--- | :--- |
| **Description** | Architectural discovery for projects starting without a BRD. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `dependency-manager`
| Property | Value |
| :--- | :--- |
| **Description** | Automated software dependency management (Node.js, Python, Git). |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `dev-engineer`
| Property | Value |
| :--- | :--- |
| **Description** | General implementation logic, debugging, and code optimization. |
| **Personas** | Python Backend, React Frontend |
| **Capabilities** | LLM: ✓ |

#### `devops-engineer`
| Property | Value |
| :--- | :--- |
| **Description** | Infrastructure as Code, CI/CD pipeline automation, and orchestration. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `diagram-manager`
| Property | Value |
| :--- | :--- |
| **Description** | Specialized skill for creating and maintaining visual documentation (Mermaid). |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `documenter`
| Property | Value |
| :--- | :--- |
| **Description** | External document generation and publishing (Google Docs). |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `enterprise-architect`
| Property | Value |
| :--- | :--- |
| **Description** | High-level alignment, capability mapping, and strategic governance. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `git-manager`
| Property | Value |
| :--- | :--- |
| **Description** | Automated Git operations and commit message generation. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ / CLI: ✓ |

#### `ignore-manager`
| Property | Value |
| :--- | :--- |
| **Description** | Create and manage .ignore files for the project. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `librarian`
| Property | Value |
| :--- | :--- |
| **Description** | Evolution and maintenance of the Gemini CLI environment and metadata. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `prompting`
| Property | Value |
| :--- | :--- |
| **Description** | Assists in crafting precise, deterministic, and high-quality prompts. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `researcher`
| Property | Value |
| :--- | :--- |
| **Description** | Context-aware synthesis of technical, structural, and commercial research. |
| **Personas** | Architect, Engineer, DevOps, Finance/Commercial |
| **Capabilities** | LLM: ✓ |

#### `secretary`
| Property | Value |
| :--- | :--- |
| **Description** | Meeting notes, action items, and decision extraction. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ / CLI: ✓ |

#### `skill-creator`
| Property | Value |
| :--- | :--- |
| **Description** | Guide for creating effective skills that extend Gemini CLI's capabilities. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `solution-architect`
| Property | Value |
| :--- | :--- |
| **Description** | High-level design, trade-off analysis (Event-Driven, Edge). |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `system-analyst`
| Property | Value |
| :--- | :--- |
| **Description** | Gap analysis, state transitions, and requirements extraction. |
| **Personas** | N/A |
| **Capabilities** | LLM: ✓ |

#### `auditor`
| Property | Value |
| :--- | :--- |
| **Description** | Unified auditing for structural integrity, performance, prompts, and compliance. |
| **Personas** | Structural, Performance, Prompt, Compliance |
| **Capabilities** | LLM: ✓ / CLI: ✓ |

## Executable Scripts

| Topic Name                | Values/Description                                        | LLM | CLI |
| :------------------------ | :-------------------------------------------------------- | :-: | :-: |
| `audit_structure.cjs`     | Audits the workspace for naming and structure violations. |     |  ✓  |
| `prepare_commit.cjs`     | Captures Git diffs and scaffolds commit summary tasks.    |  ✓  |  ✓  |
| `validate_skill.cjs`      | Validates a skill's SKILL.md for schema compliance.       |     |  ✓  |
| `log_improvement.cjs`     | Records recurring patterns for instruction optimization.  |  ✓  |  ✓  |
| `format_meeting_notes.py` | Cleans up and formats raw meeting notes or transcripts.   |  ✓  |  ✓  |
| `publish_to_gdocs.cjs`   | Syncs local Markdown files to Google Docs (via ADC).      |  ✓  |  ✓  |

*Note: Executable scripts are located in the `scripts/` directory of their respective skills (e.g., `skills/auditor/scripts/` or `skills/git-manager/scripts/`).*

## Templates

| Topic Name | Values/Description | Owner |
| :--- | :--- | :--- |
| `SKILL.template.md`                   | Boilerplate for creating new specialized skills.  | `skill-creator`  |
| `hld.template.md`                     | Master template for High-Level Design documents.  | `solution-architect` |
| `hld-*.template.md`                   | Modular components for HLDs (header, footer, etc).| `solution-architect` |
| `changes.template.md`                 | Format for recording architectural modifications. | `librarian`      |
| `discovery.template.md`               | Structure for deep-dive research findings.        | `librarian`      |
| `change-log.template.md`              | Template for the central system change log.       | `librarian`      |
| `discovery-log.template.md`           | Template for the research task tracking log.      | `librarian`      |
| `folder-structure.template.md`        | Template for maintaining workspace structural map.| `auditor`        |
| `as-is-to-be.template.md`             | Framework for mapping state transitions.          | `system-analyst` |
| `gap-analysis.template.md`            | Template for identifying missing capabilities.    | `system-analyst` |
| `requirements-extraction.template.md` | Format for drafting functional requirements.      | `system-analyst` |
| `friction-points.template.md`         | Template for identifying system bottlenecks.      | `system-analyst` |
| `audit-report.template.md`            | Template for structural and performance reports.  | `auditor`        |
