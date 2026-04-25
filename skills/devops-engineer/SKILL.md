---
name: devops-engineer
description: DevOps and IaC — apply infrastructure-as-code, CI/CD, cloud patterns, and Terraform discovery/HCL. Invoke for pipelines, remote state, modules, or IaC scan/scaffold; use cloud-engineer for live cloud inventory.
metadata:
  version: "1.1"
  disable-model-invocation: true
---
# DevOps (SME + IaC)

**Main brain:** this file. **Terraform subflows** (full HCL and A/B): `workflows/terraform-main.md`, `workflows/terraform-scan.md` · **Standards:** `references/pwd-terraform-standards.md`, `references/terraform-standards.md`, `references/signal-to-resource-map.md` · **Live cross-check** (optional): `cloud-engineer` `workflows/cloud-inventory.md`.

> **Tool note:** bundled workflows and standards default to **Terraform / HCL**. For other IaC tools (Pulumi, CDK, Bicep, etc.) adapt the scan and scaffold workflows accordingly. Cloud provider configuration lives in `cloud-engineer`'s `SKILL.md`.

| Step | File |
|------|------|
| Codebase **scan** / discovery | `workflows/terraform-scan.md` |
| **Bootstrap** / scaffold (with optional live cloud inventory merge) | `workflows/terraform-main.md` |

## IaC, CI/CD, observability (summary)

- **Modular split:** `foundation` (IAM, network, storage, secrets) vs `workload` (compute, scheduling) — never mix.
- **State:** remote in shared/prod; no local state in team envs. Plans before `apply` — user reviews; `destroy` and applies need explicit OK.
- **CI/CD:** YAML pipelines; security scanning; workload identity / OIDC — no static keys.
- **Observability:** structured logs, metrics/alerts, health checks, dashboards, SLO/SLA.
- **GitOps:** git as source of truth; every change has a verifiable plan/diff before apply.

**Coordinate with** `cloud-engineer` for live cloud state and `security` for scanning policy. When a resource needs a big product/architecture call, pause and bring in `architect`.
