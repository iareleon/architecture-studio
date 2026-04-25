---
name: tester
description: Apply QA expertise to generate unit/integration tests and define testing strategy. Invoke when writing tests for new features, validating bug fixes, or setting up test suites.
metadata:
  version: "1.0"
  disable-model-invocation: true
---
# QA & Tester Expertise

**Main brain:** this file. Aligns with `development-engineer` for domain vs adapter tests.

## Strategy

- **TDD** where practicable. **Test pyramid:** many unit, fewer integration, minimal E2E. Every feature or fix ships with a validation test suite.
- **Unit:** **domain** logic only—pure Python/TypeScript, no I/O. pytest / Jest or Vitest. **Target:** strong branch coverage on domain; prefer parameterised cases.
- **Integration:** **adapters** (cloud, DB, HTTP)—**real** or **containerised** dependencies; do **not** mock infra in integration tests. Use emulators (Pub/Sub, Firestore, etc.) when available. Test error paths: network fail, permission denied, bad payload.
- **CI:** all tests pass before merge; integration may be a stage but must gate release. No test gate bypass.

## Quality

- Names: `test_<unit>_<condition>_<expected>`. **AAA** explicit—no hidden arrange in setUp. Assert **behaviour**, not private implementation. **Validate** error handling and trace propagation in adapter suites.

## Summary constraints

- 100% branch goal on **domain** logic. Features/fixes need tests. Integration tests for adapters (mocks or real test instances for externals in **unit** only where appropriate; integration stays real).

Coordinate with `development-engineer` for stack conventions.
