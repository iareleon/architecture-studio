# High-Level Design Footer (Cross-Cutting & Governance)

**Status: {{DOCUMENT_STATUS}}**

## Cross-Cutting Concerns (NFRs)
<table width="100%">
  <thead>
    <tr>
      <th align="left">Category</th>
      <th align="left">Requirement / Description</th>
      <th align="left">Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Scalability</b></td>
      <td>{{SCALABILITY_DESCRIPTION}}</td>
      <td>{{SCALABILITY_IMPACT}}</td>
    </tr>
    <tr>
      <td><b>Availability</b></td>
      <td>{{AVAILABILITY_DESCRIPTION}}</td>
      <td>{{AVAILABILITY_IMPACT}}</td>
    </tr>
    <tr>
      <td><b>Security / Data Privacy</b></td>
      <td>{{SECURITY_DESCRIPTION}}</td>
      <td>{{SECURITY_IMPACT}}</td>
    </tr>
  </tbody>
</table>

## Deployment & Operational Considerations
<table width="100%">
  <thead>
    <tr>
      <th align="left">Strategy Phase</th>
      <th align="left">Focus</th>
      <th align="left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Crawl</b></td>
      <td>Manual Integration</td>
      <td>{{CRAWL_DESCRIPTION}}</td>
    </tr>
    <tr>
      <td><b>Walk</b></td>
      <td>Automated Data</td>
      <td>{{WALK_DESCRIPTION}}</td>
    </tr>
    <tr>
      <td><b>Run</b></td>
      <td>Fully Automated</td>
      <td>{{RUN_DESCRIPTION}}</td>
    </tr>
  </tbody>
</table>

## Key Architectural Decisions (KADs)
<table width="100%">
  <thead>
    <tr>
      <th align="left">Decision</th>
      <th align="left">Justification</th>
      <th align="left">Trade-offs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>{{KAD_1_NAME}}</b></td>
      <td>{{KAD_1_JUSTIFICATION}}</td>
      <td>{{KAD_1_TRADEOFF}}</td>
    </tr>
  </tbody>
</table>

## Architectural Design Decisions (ADDs)
<table width="100%">
  <thead>
    <tr>
      <th align="left">Decision</th>
      <th align="left">Justification</th>
      <th align="left">Constraints / Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>ADD 1.1: {{ADD_1_NAME}}</b></td>
      <td>{{ADD_1_JUSTIFICATION}}</td>
      <td>{{ADD_1_CONSTRAINT}}</td>
    </tr>
  </tbody>
</table>

## Proven Method of Success (PMoSs)
<table width="100%">
  <thead>
    <tr>
      <th align="left">ID</th>
      <th align="left">Success Method</th>
      <th align="left">Reference / Validation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>PMoS 1.1</b></td>
      <td>{{PMOS_1_DESCRIPTION}}</td>
      <td>Linked to <b>ADD 1.1</b></td>
    </tr>
  </tbody>
</table>

## Architectural Risks
<table width="100%">
  <thead>
    <tr>
      <th align="left">Risk</th>
      <th align="left">Impact</th>
      <th align="left">Probability</th>
      <th align="left">Mitigation Strategy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>{{RISK_1_NAME}}</b></td>
      <td>{{RISK_1_IMPACT}}</td>
      <td>{{RISK_1_PROBABILITY}}</td>
      <td>{{RISK_1_MITIGATION}}</td>
    </tr>
  </tbody>
</table>

## Open Questions / Dependencies
<table width="100%">
  <thead>
    <tr>
      <th align="left">Question / Dependency</th>
      <th align="left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Stakeholder Assignment</b></td>
      <td>Identify the names for the following project roles: {{REQUIRED_ROLES}}.</td>
    </tr>
  </tbody>
</table>

## Development Impact Summary
<table width="100%">
  <thead>
    <tr>
      <th align="left">Component / Service</th>
      <th align="left">Status</th>
      <th align="left">Functional / Change Description</th>
      <th align="left">Primary Team</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>{{COMPONENT_NAME}}</b></td>
      <td>{{COMPONENT_STATUS}}</td>
      <td>{{COMPONENT_DESCRIPTION}}</td>
      <td>{{COMPONENT_TEAM}}</td>
    </tr>
  </tbody>
</table>

## Audit & Change History
<table width="100%">
  <thead>
    <tr>
      <th align="left">Log Type</th>
      <th align="left">Link</th>
      <th align="left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Master Changelog</b></td>
      <td>[[llm-memory/changelog|Project Changelog]]</td>
      <td>Chronological summary of all architectural and document changes.</td>
    </tr>
    <tr>
      <td><b>Detailed Audit Logs</b></td>
      <td>[[changes/|Audit Records]]</td>
      <td>Raw session logs and detailed change justifications.</td>
    </tr>
  </tbody>
</table>

---
**Navigation:**
*   **Back to:** [[hld-macro-overview|Macro Architecture Overview]]
*   **Reference:** [[discovery-log|Discovery Log]]
*   **Full Index:** [[hld-header|HLD Main Header]]
