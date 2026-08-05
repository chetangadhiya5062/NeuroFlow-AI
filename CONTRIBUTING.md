<!--
File: CONTRIBUTING.md
Project: NeuroFlow AI
-->

# Contributing to NeuroFlow AI

Thank you for your interest in contributing to **NeuroFlow AI**.

NeuroFlow AI is an enterprise-grade modular AI platform designed around strict **Clean Architecture**, **SOLID principles**, and **Domain-Agnostic Engine Design**. We welcome community contributions that align with our engineering standards and architecture specifications.

---

## Code of Conduct

All contributors must adhere to our [**Code of Conduct**](CODE_OF_CONDUCT.md).

---

## Architectural Integrity First

Before submitting code, please familiarize yourself with our core architecture baseline:
- [**Architecture Baseline**](docs/architecture/ARCHITECTURE-BASELINE.md)
- [**Implementation Blueprint**](docs/implementation/implementation-blueprint.md)
- [**Engineering Standards**](docs/development/engineering-standards.md)

### Key Rules
1. **Interface-First:** All core interfaces (`IXxxPort`) reside in `backend/core/ports/` and must be approved before implementation adapters are written.
2. **Layer Inversion:** Layer 3 runtimes depend on Layer 0 ports, never on concrete Layer 1 infrastructure.
3. **No Upward Imports:** Verified via `import-linter` in CI. Presentation or application layers cannot be imported into Layer 3 runtimes or Layer 0 core.
4. **Module Boundaries:** No single module file should exceed 300 lines of code.

---

## Development Workflow

1. **Fork the Repository:** Create a personal fork on GitHub.
2. **Clone & Set Up:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/NeuroFlow-AI.git
   cd NeuroFlow-AI
   ```
3. **Create a Feature Branch:**
   ```bash
   git checkout -b feat/task-description
   ```
4. **Implement Changes:** Write implementation code, port interfaces, and unit/integration tests following [**Engineering Standards**](docs/development/engineering-standards.md).
5. **Run Local Validation:** Ensure linting, type checks, and tests pass before committing.
6. **Submit a Pull Request:** Open a PR against the `main` branch.

---

## Branch Naming Conventions

Use lowercase branch names prefixed with the change category:

| Prefix | Category | Example |
| :--- | :--- | :--- |
| `feat/` | New feature or capability | `feat/qdrant-vector-adapter` |
| `fix/` | Bug fix | `fix/workflow-state-checkpoint-race` |
| `docs/` | Documentation update | `docs/update-rag-runtime-spec` |
| `refactor/` | Code refactoring (no behavioral change) | `refactor/prompt-compiler-pipeline` |
| `test/` | Adding or updating test suites | `test/contract-event-bus-kafka` |
| `chore/` | Tooling, dependencies, or maintenance | `chore/update-uv-lock` |

---

## Commit Conventions

NeuroFlow AI enforces **Conventional Commits (v1.0.0)**. Commit messages must be structured as follows:

```
<type>(<scope>): <short summary>

[optional body text detailing rationale]

[optional footer(s), e.g., Closes #123]
```

### Commit Types
- `feat`: A new platform feature or port interface.
- `fix`: A bug fix in runtime, infrastructure, or services.
- `docs`: Documentation changes only.
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `test`: Adding missing tests or correcting existing tests.
- `chore`: Maintenance, CI configuration, or dependency updates.

### Examples
```bash
feat(rag): add multi-modal hybrid retrieval fusion pipeline
fix(workflow): resolve saga compensation rollback state transition bug
docs(arch): update Platform Runtime v2.0.0 specification references
test(infra): add contract conformance tests for RedisTaskQueueAdapter
```

---

## Pull Request Process

1. **Self-Review:** Review your diff against [**Engineering Standards**](docs/development/engineering-standards.md).
2. **CI Gates Must Pass:**
   - **Lint:** `ruff check .` and `ruff format --check .`
   - **Type Checking:** `mypy backend` (0 errors)
   - **Layer Architecture:** `import-linter` (0 violations)
   - **Unit Tests:** `pytest tests/unit/` (coverage gate enforced)
   - **Contract Tests:** `pytest tests/contract/`
3. **PR Description:** Include a clear summary of what was changed, motivation, issue numbers closed, and how it was tested.
4. **Squash-Merge:** PRs are squash-merged into `main` to maintain a clean commit history.

---

## Code Review Expectations

All Pull Requests require approval from at least one Core Maintainer or Lead Architect. Code reviews focus on:
- Strict compliance with Clean Architecture boundaries.
- Full unit and contract test coverage for all new adapters and runtimes.
- Proper JSON-structured logging and OpenTelemetry trace propagation.
- Absence of hardcoded configuration or third-party framework leaks into Layer 3.
