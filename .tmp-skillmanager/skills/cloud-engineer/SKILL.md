---
name: cloud-engineer
description: Cloud infrastructure — read-only discovery, inventory, and SME baseline for your configured cloud provider. Invoke for project inventory, scan flows, and cloud architecture defaults.
metadata:
  version: "1.1"
  disable-model-invocation: true
---
# Cloud engineer (router)

**Main brain:** this file.

> **Provider note:** bundled workflows and discovery commands default to **GCP / gcloud**. For other providers (AWS, Azure, etc.) replace `references/gcloud-discovery-commands.md` with your provider's CLI and service equivalents. All principles below are provider-agnostic.

| Task | Load |
|------|------|
| Live **inventory** (as-is, IaC input) | `workflows/cloud-inventory.md`, `references/gcloud-discovery-commands.md` |
| **Standards** / design only (no live session) | this file |

## Always (inventory and advice)

- Confirm **target project / account / subscription** before queries or recommendations. Always scope queries to avoid cross-environment leakage.
- **Read-only** in inventory: use list, describe, and policy-read commands only — never mutating commands here.
- If a command fails (permission denied, API not enabled), note it and continue.
- **IAM:** least privilege at narrowest scope; Workload Identity / OIDC federation only — **no** long-lived static credentials or key files; never owner/admin roles on automation SAs; justify all bindings.
- **Resources:** prefer managed, provider-native services; enable only required APIs/services; private networking by default; no public endpoints without justification.
- **Cost:** call out cost implications of new resources.

## Service areas to scan (inventory)

Serverless compute, managed databases, object storage, messaging/queuing, secrets management, IAM principals and bindings, networking (VPC/subnet/firewall), container registries. Extend the list per project and provider.

## Workflow expectations

- Output structured inventory by service area when harvesting.
- **Mutating** cloud CLI or console-apply flows are **out of scope** here — use runbooks, pipelines, or dedicated automation. This skill is read-only and advisory for inventory and standards.
