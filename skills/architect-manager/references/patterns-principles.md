---
name: architect
description: Patterns and design principles for custom software — Hexagonal/ports-and-adapters, layering, DI, and refactor discipline. Load when designing or reviewing service/module structure.
metadata:
  version: "1.0"
  disable-model-invocation: true
---
# Patterns and principles

Load for **bespoke code** (services, modules, strong domain boundaries). Do not force ports/adapters on integration architecture, data platforms, or package-led solutions.

**Coordinate** with `security` for platform IAM, secret stores, and scanning.

## Hexagonal (ports and adapters)

**Principles:**
- **SoC:** strict boundaries — Domain / Application (ports) / Infrastructure (adapters).
- **Domain isolation:** domain logic agnostic of external drivers (DB, API, UI, CLI).
- **Interface-driven:** depend on abstractions; inject external dependencies.
- **Statelessness:** prefer functional purity where it simplifies testing and scaling.

**Design standards:**
- Infrastructure must not leak into domain.
- Propose ports before adapters; validate against principles before presenting.
- Prefer explicit composition and injected dependencies over service locators and hidden globals.

## Refactoring

- If a bug traces to SRP/SoC violation, propose a refactor — not a surface patch. Refactors need their own plan and approval; never bundle silently.
- Prefer incremental refactors over big-bang rewrites.

## Security at the application boundary

- Zero-trust: verify at every boundary; least privilege in code.
- Never hardcode secrets — use stack-level injection. See `security` for policy and platform patterns.
- Follow organisational crypto and classification policy for data at rest or in flight.

## Where this pattern fits

Event-driven boundaries and clear component responsibilities pair well with hexagonal cores. Keep domain free of transport concerns via ports regardless of deployment edge or latency shape.

**AI / ML services are infrastructure** — model inference endpoints, vector stores, and embedding APIs belong behind ports. The domain never imports a provider SDK directly; adapters handle provider coupling and can be swapped as models evolve.

When stakeholders need HLD text, use the `document` skill and its `references/hld-templates/`.
