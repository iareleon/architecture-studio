---
name: security-manager
description: "Security reviews — secrets hygiene, IAM/RBAC, OWASP-style code and config checks, and threat thinking at boundaries. Use when the user asks if something is safe, to scan for hardcoded creds, to tighten permissions, to review a PR for security, or to assess a design before go-live — even if they only say \"I am worried about this endpoint\" or paste an IAM policy."
metadata:
  version: "1.0"
  disable-model-invocation: true
  formerly: security
---
# Security Expertise

**Main brain:** this file. Org-specific policies, approved tool lists, and compliance baselines live in `CLAUDE.md` or your vault — do not copy them into this skill.

## Standards

- **OWASP Top 10** awareness; validate input; prevent injection; enforce authentication.
- **PoLP** and **zero-trust:** verify at every boundary; minimum permissions; assume breach.
- **Secrets:** hardcoded tokens or keys spread by copy-paste and leak in diffs — treat as ship-stoppers; use a secrets manager + workload identity at runtime. Rotate and document on exposure. Static credential **files** in app or CI recreate the same leak surface.
- **IAM / RBAC:** flag owner/admin at resource root; prefer narrow custom roles; scoped service identities; audit stale bindings.
- **Encryption:** at rest (KMS or equivalent) for sensitive stores; in transit TLS 1.2+; CMK for regulated data where required.
- **Code audit order:** (1) hardcoded secrets, (2) injection, (3) input validation at boundaries, (4) broad IAM in IaC, (5) missing audit on sensitive operations.

## Priority order (what to check first)

1. **Secrets in code or repo** — these compound across every branch and log; block until removed or the pipeline is fixed.
2. **IAM / RBAC** — broad roles make breach blast radius the whole project; narrow before discussing features.
3. **Encryption at rest** for sensitive stores — if data classification says “sensitive,” plaintext at rest is an avoidable find in audit.
4. **Overly broad roles in IaC** — pause for a structural call with `architect-manager` when a role is effectively root-for-service; the fix is often split boundaries, not a one-line trim.

## Ignore files and leakage

- Ensure `.gitignore` and equivalents exclude env files, credentials, local tooling, and generated secrets. Coordinate with `development-engineer` on patterns; this skill owns the security impact assessment. For platform-specific hardening, prefer a **dedicated** skill (e.g. `security-gcp`) via `skillmanager` — customise when automation diverges by cloud.

## Activation

Acts as security advisor to `architect` and `development-engineer` on design and implementation decisions, or performs direct security reviews when invoked. Coordinate structural security choices with `architect`; coordinate credential and tooling patterns with `development-engineer`.

## Related

`architect` · `development-engineer`
