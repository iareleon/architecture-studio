# Systems Matrix

**Status: {{DOCUMENT_STATUS}}**

This table maps each business activity to the system responsible for it.

<table width="100%">
  <thead>
    <tr>
      <th align="left">Business Activity</th>
      <th align="left">System / Application Component</th>
    </tr>
  </thead>
  <tbody>
    <tr><td colspan="2"><b>[[hld-p1-{{PHASE_1_SLUG}}|Phase 1: {{PHASE_1_NAME}}]]</b></td></tr>
    <tr>
      <td>{{ACTIVITY_1}}</td>
      <td>{{SYSTEM_1}}</td>
    </tr>
    <tr>
      <td>{{ACTIVITY_2}}</td>
      <td>{{SYSTEM_2}}</td>
    </tr>
    <tr><td colspan="2"><b>[[hld-p2-{{PHASE_2_SLUG}}|Phase 2: {{PHASE_2_NAME}}]]</b></td></tr>
    <tr>
      <td>{{ACTIVITY_3}}</td>
      <td>{{SYSTEM_3}}</td>
    </tr>
  </tbody>
</table>

## Component Usage Diagrams

### {{SYSTEM_1}}
```mermaid
graph TD
    Act1[{{ACTIVITY_1}}]:::activity
    Act2[{{ACTIVITY_2}}]:::activity
    Sys[{{SYSTEM_1}}]:::system
    Act1 -->|Uses| Sys
    Act2 -->|Uses| Sys

    classDef system fill:#005A9C,stroke:#fff,stroke-width:2px,color:#fff;
    classDef activity fill:#0085CA,stroke:#fff,stroke-width:2px,color:#fff;
```

---
**Navigation:**
*   **Back to:** [[hld-macro-overview|Macro Architecture Overview]]
*   **Reference:** [[discovery-log|Discovery Log]]
*   **Full Index:** [[hld-header|HLD Main Header]]