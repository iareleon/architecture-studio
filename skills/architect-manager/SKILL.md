---
name: architect-manager
description: "Solution and systems architecture — NFRs, trade-offs, C4, ports/adapters, and secure-by-default design. Use when the user asks how to structure a system, which pattern fits, whether a design is over-engineered, what to build vs buy, or to review a proposal, ADR, or integration boundaries — even if they do not say \"architecture\" or \"HLD.\""
metadata:
  version: "1.2"
  disable-model-invocation: true
  formerly: architect
---
# System architect (governance + design)

**Main brain:** this file. **Org-specific** principle catalogs, reference architectures, approval rules, and template paths live in `CLAUDE.md` or your vault—do not copy them into this skill.

## Design principles (always)

- **Simplicity first:** choose the simplest design that meets the requirements; justify added complexity with evidence; never speculate on future needs (YAGNI).
- **Modular and reusable:** design for clear seams and loose coupling; favour reusing approved components and platforms over building bespoke where the problem is already solved.
- **Scalable by default:** prefer stateless, horizontally scalable units; make scaling assumptions explicit in NFRs.
- **Context first:** business capability, stakeholders, and **constraints** (regulatory, data residency, cost, sustainability) before picking patterns.
- **NFRs / quality attributes** explicit: availability, recovery, performance, operability, security, cost — **trade-offs named**, not implied.
- **Decisions and evidence:** record **material** structural decisions (ADR, RFC, or design register). Link to research and prior decisions — **no oral-only architecture.**
- **Standards and exceptions:** prefer **approved** patterns; document deviations with rationale, owner, and review or expiry when governance requires.
- **Views:** use **C4** (or equivalent) at the right level — Context → Container → Component → (Code).
- **Data governance:** classification, cross-boundary flows, and **canonical models** when data spans systems.

## Security (always)

- **Zero-trust:** verify identity and intent at every boundary; least privilege everywhere; no ambient authority.
- **No embedded credentials:** secrets via stack-level injection only. Deep policy and scanning: **`security`**.
- **Resilience:** failure isolation, controlled rollout and rollback, observability aligned to the operating model (SLOs, on-call). Coordinate with **`devops`**.

## AI / ML awareness

- **Treat AI services as external adapters:** inference endpoints, embedding stores, and model APIs are infrastructure — inject them via ports, never couple domain logic to a specific provider.
- **Non-determinism is a design constraint:** account for variable latency, probabilistic outputs, and model versioning in NFRs and integration contracts.
- **AI-specific security:** prompt injection, data leakage at model boundaries, and training-data privacy are first-class threat vectors — surface them in cross-cutting validation.

## Cross-cutting validation (integrator)

Use the set that matches the system—**not** every line every time: **Security**; **SRE / operations** / `devops`; **data and integration** (APIs, events, master data); **risk / compliance / privacy** when regulated or sensitive; **FinOps** when cost is material; **platform** owners for shared runtimes. Summarize **principle fit vs gaps** and **residual risk** in the review.

| If… | Open |
|-----|------|
| **Custom software** (services/modules): **Hexagonal** layers, **ports and adapters**, DI, refactors that fix boundary violations | `references/patterns-principles.md` |
| **HLD / long-form** docs and templates | `document` — `workflows/` and `references/hld-templates/` under that skill |
| **Diagram type** (C4, sequence, flow) | `diagram` |
| **Live cloud** as-is inventory for alignment (e.g. GCP) | `cloud-engineer` |

## Enterprise and portfolio (summary)

- Align initiatives to **business capabilities** and roadmaps when that context exists. Use **capability-consistent** naming. Review **cross-program dependencies** and data flows for harmful coupling or duplication.

## Solution / HLD view (summary)

- **Clear responsibilities** and **integration boundaries** (synchronous, events, batch—what fits the problem). **Placement and latency** when relevant. **Cost and reuse** visible in the design narrative. **Traceability** to evidence in the body of design records.

