# ADR-014: Implementation Blueprint & Module Naming Resolution

- **Status:** Accepted
- **Date:** 2026-08-05
- **Deciders:** Principal Software Architect, Lead Architect
- **Technical Story:** Architecture Implementation Readiness & Pre-Commit Governance

---

## Context

The Phase 1 architecture of NeuroFlow AI is complete and frozen across twelve runtime and layer specifications. A comprehensive architecture review (Readiness Score: 88/100 — GREEN) identified four critical pre-implementation governance items ("MUST FIX"):

1. **Module Naming Ambiguity:** Scaffolding directories (`backend/workflows/`, `backend/agents/`, `backend/rag/`, `backend/ai/`) collided with or diverged from canonical runtime names defined in architecture documents (`backend/workflow_engine/`, `backend/agent_runtime/`, `backend/rag_runtime/`, `backend/llm_gateway/`).
2. **Plugin SDK Architecture Gap:** Missing specification for `NeuroFlowPluginContext`, plugin lifecycle hooks, and sandboxing rules (addressed in ADR-015 / `docs/architecture/plugin-sdk.md`).
3. **Unconfirmed Port Declarations:** `IRAGRuntime` and `IPromptRuntime` ports needed explicit Layer 0 confirmation.
4. **Agent-Prompt Delegation Boundary:** Delegation between Agent Runtime reasoning and Prompt Runtime context assembly required explicit scoping.

To begin backend implementation cleanly without technical debt, a formal implementation sequence and module naming resolution must be declared.

---

## Decision

1. **Adopt Canonical Module Names:**
   - Rename `backend/workflows/` → `backend/workflow_engine/`
   - Rename `backend/agents/` → `backend/agent_runtime/`
   - Rename `backend/rag/` → `backend/rag_runtime/`
   - Rename `backend/ai/` → `backend/llm_gateway/`

2. **Milestone-Based Sequential Build Order:**
   Implementation must proceed strictly through 9 incremental milestones:
   - **Milestone 0:** Foundation & Tooling (`pyproject.toml`, `import-linter`, CI)
   - **Milestone 1:** Core Contracts (`backend/core/ports/`, domain entities, exceptions)
   - **Milestone 2:** Infrastructure Adapters (`sql/`, `cache/`, `vector/`, `graph_db/`, `llm/`, `event_bus/`)
   - **Milestone 3:** Storage Runtimes (`knowledge_base/`, `knowledge_graph/`, `memory_layer/`)
   - **Milestone 4:** Retrieval & Prompt Layer (`rag_runtime/`, `prompt_runtime/`, `llm_gateway/`)
   - **Milestone 5:** Execution Engines (`tool_runtime/`, `integration_runtime/`, `workflow_engine/`)
   - **Milestone 6:** Intelligence Layer (`agent_runtime/`)
   - **Milestone 7:** Platform Integration (`services/`, `api/`, `plugins/telecom/`)
   - **Milestone 8:** Production Hardening (Load testing, security, deployment)

3. **Interface-First Enforcement:**
   Every subsystem follows a 9-step sequence: Port Interface → Lead Architect Review → Domain Models → Infra Adapters & Contract Tests → Runtime Module → DI Binding → Service → API Endpoint → E2E Test.

4. **Architectural Guardrails:**
   - Enforce `.importlinter` rules in CI from Day 1 to prevent upward imports.
   - Core ports in `backend/core/ports/` require Lead Architect approval for any modification.

---

## Consequences

### Positive
- **Zero Technical Debt:** Naming collisions resolved prior to first commit.
- **Predictable Order:** Modular monolith built in strict dependency-depth order.
- **Enforced Layering:** Clean Architecture strictly validated at build time via `import-linter`.

### Negative
- **Upfront Governance Overhead:** Requires completing prerequisite governance tasks in Milestone 0 prior to business logic commits.

---

## References
- `docs/implementation/implementation-blueprint.md`
- `docs/development/engineering-standards.md`
- `docs/architecture/ARCHITECTURE-BASELINE.md`
