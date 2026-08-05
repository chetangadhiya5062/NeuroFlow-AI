# NeuroFlow AI — Engineering Standards

**Document Version:** 1.0.0
**Status:** Approved Engineering Guide
**Target Audience:** All Software Engineers contributing to NeuroFlow AI

---

## 1. Coding Philosophy

NeuroFlow AI is built on rigorous engineering standards. 
- **Readability over cleverness**: Code is read orders of magnitude more often than it is written.
- **Explicit is better than implicit**: Avoid magic behavior, hidden state, and obscured dependencies.
- **Interface-First**: Contracts define boundaries. Implementations are just details.

## 2. Code Quality Expectations

- **Static Typing**: 100% strict type hints enforced via MyPy. No `Any` types without an explicit inline `# type: ignore` accompanied by a justification.
- **Linting**: 100% compliance with `ruff` rules. 
- **Module Size**: Modules should ideally not exceed 300 lines of code. If a module grows larger, it is a candidate for refactoring.
- **Function Size**: Functions should do one thing and fit on a single screen.

## 3. SOLID Expectations

- **Single Responsibility**: Each class/module must have only one reason to change.
- **Open/Closed**: Runtimes must be open for extension (via plugins) but closed for modification.
- **Liskov Substitution**: Any infrastructure adapter must be perfectly substitutable for its port without breaking consumer expectations.
- **Interface Segregation**: Do not force clients to depend on methods they do not use. 
- **Dependency Inversion**: High-level modules must not depend on low-level modules. Both must depend on abstractions (ports).

## 4. Dependency Injection Principles

NeuroFlow AI uses a **constructor-injection** model throughout.
- Never instantiate dependencies inside a class constructor.
- Never use global singletons for stateful services.
- All concrete adapter choices are made at application startup through environment variables. No hardcoded adapter names appear in runtime modules.

## 5. Testing Expectations

- **Test Pyramid**: ~60% Unit, ~25% Integration, ~10% Contract, ~5% E2E.
- **Unit Tests**: No I/O. Use mocks or in-memory adapters.
- **Integration Tests**: Require real infrastructure via Docker Compose.
- **Contract Tests**: Every adapter must pass the shared contract test for its implemented port.
- **Coverage Gates**: `core` (100%), `infrastructure` (90%), `runtimes` (85%), `services` (85%), `api` (80%), `plugins/sdk` (95%). Enforced in CI.

## 6. Performance Expectations

- **API Latency**: p99 latency < 2s for agent invocations under load (100 concurrent).
- **Retrieval Latency**: p95 retrieval latency < 500ms in Docker environment.
- **Throughput**: Non-blocking asynchronous I/O must be used for all external calls.

## 7. Documentation Standards

- 100% docstring coverage on all public interfaces and port contracts.
- Use Google-style docstrings.
- Update `README.md` files when module boundaries or purposes change.
- Document complex algorithms with inline comments explaining *why*, not *what*.

## 8. Logging Standards

- **Structured Logging**: All log output is **JSON-structured** in non-development environments.
- **Levels**:
  - `DEBUG`: Detailed execution tracing. Development only.
  - `INFO`: Normal platform operation events.
  - `WARNING`: Recoverable abnormal conditions (retry attempt).
  - `ERROR`: Failures requiring attention.
  - `CRITICAL`: Platform-level failures.
- **Correlation**: Every log line in a request context must carry `trace_id` and `span_id` from the OpenTelemetry context.

## 9. Error Handling Standards

- **Never swallow exceptions silently.** 
- **Infrastructure errors are wrapped.** Raw exceptions (e.g., `redis.ConnectionError`) must be caught and re-raised as `InfrastructureError`.
- **API Errors**: All API errors return structured JSON mapped via global FastAPI exception handlers.
- **Retryable explicitly**: Every `ExecutionError` subclass must declare if it is retryable.

## 10. Code Review Checklist

Before approving a PR, reviewers must verify:
- [ ] Layer boundaries are respected (no upward imports).
- [ ] No concrete infrastructure is imported directly in Layer 3.
- [ ] Tests cover happy path, edge cases, and error handling.
- [ ] New exceptions subclass `PlatformError`.
- [ ] Log levels are appropriate and structured.

## 11. Pull Request Checklist

Authors must ensure:
- [ ] CI pipeline passes (MyPy, Ruff, Tests, Coverage).
- [ ] import-linter passes successfully.
- [ ] Feature branches are short-lived (max 3 days).
- [ ] Commits follow Conventional Commits format (`feat:`, `fix:`, `docs:`, etc.).
- [ ] Squash-merge is used when merging to `main`.
