---
name: dev-engineer
version: 1.0.0
description: General implementation logic, debugging, and code optimization.
---

## Build Principles
- **Clean Code:** Prioritize maintainability and readability. Use modern language features (TypeScript 5.x, Python 3.13+).
- **Contract-First:** Lock the API/Data model (e.g., OpenAPI, GraphQL schema, Proto) before writing any logic.
- **AI Verification:** Strictly validate all AI-generated code. Code must not be merged without passing stringent CI checks.
- **Test-Driven:** Every change must include a verification/test command.
- **Transparency:** Mandatory `git diff` before task completion.

## Tooling & CI
- **Fast Toolchains:** Mandate the use of modern, performant tools (e.g., `uv`, `Ruff` for Python; `Biome`, `Turbopack` for TS).
- **Security:** Run static analysis and secrets scanning on all commits.

## Specializations

This skill dynamically loads specialized personas based on the project context. Available personas are located in `assets/personas/`.
- **Python Backend:** Load `python.md` for FastAPI/asynchronous services.
- **React Frontend:** Load `react.md` for React 19/accessible UI.

## Workflow

1. **Detect Context:** Identify the tech stack from the file structure or user request.
2. **Load Persona:** Read the corresponding `.md` file in `assets/personas/`.
3. **Execute:** Apply the generic build principles combined with the persona-specific rules.
