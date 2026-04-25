# High-Level Architecture Overview (Macro HLD)

**Status: {{DOCUMENT_STATUS}}**
**Phases Completed: {{PHASES_COMPLETED}}**

This diagram outlines the application components participating in each stage of the lifecycle.

```mermaid
flowchart TD
    %% Main Lifecycle Flow (Force Horizontal Row)
    subgraph Lifecycle [Campaign Lifecycle Phases]
        direction LR
        P1[Phase 1:<br>{{PHASE_1_NAME}}] --> P2[Phase 2:<br>{{PHASE_2_NAME}}]
        P2 --> P3[Phase 3:<br>{{PHASE_3_NAME}}]
        P3 --> P4[Phase 4:<br>{{PHASE_4_NAME}}]
        P4 --> P5[Phase 5:<br>{{PHASE_5_NAME}}]
    end

    %% Business Components Layer (Force Horizontal Row)
    subgraph BizComp [Business Components]
        direction LR
        C1[{{BIZ_COMP_1}}]
        C2[{{BIZ_COMP_2}}]
    end

    %% Application Components Layer (Force Horizontal Row)
    subgraph AppComp [Application Components]
        direction LR
        A1[{{APP_COMP_1}}]
        A2[{{APP_COMP_2}}]
    end

    %% Layout Constraints (Invisible links to force vertical stacking of horizontal layers)
    Lifecycle ~~~ BizComp
    BizComp ~~~ AppComp

    %% Functional Links
    %% Phase 1
    P1 -->|{{DATA_FLOW_1}}| C1
    
    %% Styling
    style Lifecycle fill:#f8fafc,stroke:#cbd5e1,stroke-width:2px,stroke-dasharray: 5 5
    style P1 fill:#f9731640,stroke:#f97316,stroke-width:2px
    style P2 fill:#ef444440,stroke:#ef4444,stroke-width:2px
    style P3 fill:#22c55e40,stroke:#22c55e,stroke-width:2px
    style P4 fill:#06b6d440,stroke:#06b6d4,stroke-width:2px
    style P5 fill:#a855f740,stroke:#a855f7,stroke-width:2px

    style BizComp fill:#f1f5f9,stroke:#94a3b8,stroke-width:1px
    style AppComp fill:#f1f5f9,stroke:#94a3b8,stroke-width:1px

    classDef component fill:#ffffff,stroke:#475569,stroke-width:1px,color:#1e293b;
    class C1,C2,A1,A2 component;

    %% Link Styles based on phase colors
    linkStyle 0 stroke:#cbd5e1,stroke-width:2px;
```

## Process Overview

The lifecycle of the system involves the following main phases:

1. **{{PHASE_1_NAME}}:** {{PHASE_1_DESC}}
2. **{{PHASE_2_NAME}}:** {{PHASE_2_DESC}}
3. **{{PHASE_3_NAME}}:** {{PHASE_3_DESC}}
4. **{{PHASE_4_NAME}}:** {{PHASE_4_DESC}}
5. **{{PHASE_5_NAME}}:** {{PHASE_5_DESC}}

### Detailed Phase Descriptions

#### [[hld-p1-{{PHASE_1_SLUG}}|Phase 1: {{PHASE_1_NAME}}]]: 

```mermaid
flowchart TD
    P1[Phase 1:<br>{{PHASE_1_NAME}}]
    C1[{{BIZ_COMP_1}}]
    
    P1 -->|{{DATA_FLOW_1}}| C1
    
    style P1 fill:#f9731640,stroke:#f97316,stroke-width:2px
    classDef component fill:#ffffff,stroke:#475569,stroke-width:1px,color:#1e293b;
    class C1 component;
```

{{PHASE_1_DETAILS}}

## Navigation & References

| Description | Link |
| :--- | :--- |
| **Executive Introduction** | [[hld-introduction]] |
| **Systems Matrix** | [[hld-systems-matrix]] |
| **Discovery Log** | [[discovery-log\|Discovery Log]] |
| **Business Clarifications** | [[business-clarifications]] |
| **HLD Footer** | [[hld-footer]] |
| **Project Changelog** | [[llm-memory/changelog\|Changelog]] |
| **Audit Records** | [[changes/\|Audit Logs]] |