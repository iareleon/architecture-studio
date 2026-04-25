---
name: security
description: Apply security expertise for IAM reviews, secret management, and OWASP vulnerability assessment. Invoke when reviewing permissions, handling credentials, or auditing code for security issues.
metadata:
  version: "1.0"
  disable-model-invocation: true
---
# Security Expertise

**Main brain:** this file. Org-specific policies, approved tool lists, and compliance baselines live in `CLAUDE.md` or your vault — do not copy them into this skill.

## Standards

- **OWASP Top 10** awareness; validate input; prevent injection; enforce authentication.
- **PoLP** and **zero-trust:** verify at every boundary; minimum permissions; assume breach.
- **Secrets:** never hardcode tokens or keys—**critical block**; use secrets manager + runtime access via workload identity. Rotate and document on exposure. No static credential **files** in app or CI.
- **IAM / RBAC:** flag owner/admin at resource root; prefer narrow custom roles; scoped service identities; audit stale bindings.
- **Encryption:** at rest (KMS or equivalent) for sensitive stores; in transit TLS 1.2+; CMK for regulated data where required.
- **Code audit order:** (1) hardcoded secrets, (2) injection, (3) input validation at boundaries, (4) broad IAM in IaC, (5) missing audit on sensitive operations.

## Mandatory tasks and constraints (summary)

1. Block hardcoded secrets and credential files immediately.
2. Review IAM/RBAC for least privilege.
3. Enforce encryption at rest for sensitive data stores.
4. **Critical block** on overly broad roles. Flag for `architect` on structural security choices.

## Ignore files and leakage

- Ensure `.gitignore` and equivalents exclude env files, credentials, local tooling, and generated secrets. Coordinate with `development-engineer` on patterns; this skill owns the security impact assessment. For platform-specific hardening, prefer a **dedicated** skill (e.g. `security-gcp`) via `skillmanager` — customise when automation diverges by cloud.

## Activation

Acts as security advisor to `architect` and `development-engineer` on design and implementation decisions, or performs direct security reviews when invoked. Coordinate structural security choices with `architect`; coordinate credential and tooling patterns with `development-engineer`.

## Related

`architect` · `development-engineer`
