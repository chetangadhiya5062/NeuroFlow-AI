# ADR-012: Prompt Runtime Architecture — Enterprise Prompt Orchestration Subsystem

**Title:** Prompt Runtime Architecture — Enterprise Prompt Orchestration Subsystem  
**Status:** Accepted  
**Date:** 2026-08-04  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic Prompt Runtime as the platform's authoritative prompt orchestration subsystem, co-located in Platform Runtime (Layer 3), responsible for prompt registration, versioning, multi-stage compilation, dynamic context assembly, token budget optimization, safety policy enforcement, caching, and lineage tracking.

---

## Context

NeuroFlow AI is a production-grade modular AI Operating Platform. Following the completion of Clean Architecture, Platform Runtime, Internal Event Bus, AI Memory Layer, Knowledge Base, Knowledge Graph, Workflow Engine, Agent Runtime, Tool Runtime, and Integration Runtime architectures, the next milestone is prompt orchestration.

Before this decision, prompts were treated as inline strings or ad-hoc templates scattered across agent loops and plugin implementations. This produced significant architectural liabilities:

- **Prompt Fragmentation & Drift**: Inconsistent instructions across modules and plugins without central version control.
- **Unbounded Context Windows**: Callers constructed prompts manually, leading to context window overflows and token waste.
- **Security Vulnerabilities**: Lack of standardized input sanitization, exposing the platform to prompt injection and jailbreak attacks.
- **Missing Audit Lineage**: Inability to trace an LLM output back to the exact prompt template version and context state that produced it.

---

## Decision

**We will introduce a dedicated Prompt Runtime as a reusable Platform Runtime (Layer 3) capability.**

The Prompt Runtime is explicitly defined as:

> NeuroFlow AI's **enterprise prompt orchestration subsystem**, responsible for prompt registration, versioning, multi-stage compilation, dynamic context assembly, token budget optimization, safety policy enforcement, caching, and lineage tracking across all platform modules and domain plugins.

The Prompt Runtime is **not** a prompt template library, **not** prompt engineering, and **not** an LLM provider adapter.

Every prompt executed within NeuroFlow AI must pass through the Prompt Runtime via the `IPromptRuntime` port.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/prompt-runtime.md`) establishes the following key structures:

### Layer Placement

The Prompt Runtime resides in **Platform Runtime (Layer 3)** at `backend/prompt_runtime/`, co-located with the Agent Runtime, Tool Runtime, Workflow Engine, Knowledge Base, Knowledge Graph, and Memory Layer. Abstract contracts reside in Layer 0 (`backend/core/ports/prompt.py`), and storage adapters reside in Layer 1 (`backend/infrastructure/prompt/`).

### Nine Core Subsystems

1. **Prompt Registry**: Multi-tier versioned manifest store (PostgreSQL + Redis + Vector Store).
2. **Prompt Discovery Engine**: Dynamic semantic search and category lookup.
3. **Context Aggregator**: Fetches variables, Memory Layer state, KB chunks, KG subgraphs, and tool manifests in parallel.
4. **Prompt Compiler**: AST builder, template engine, and block merger.
5. **Safety & Policy Gate**: Injection scanning, jailbreak detection, PII masking, and system prompt protection.
6. **Token Budget Optimizer**: Dynamic token allocation matrix and priority-based AST pruning.
7. **Prompt Cache**: Redis-backed compiled AST and payload caching.
8. **LLM Target Adapter**: Provider payload formatting (OpenAI, Anthropic, Gemini).
9. **Audit & Lineage Engine**: SHA-256 cryptographic lineage hash generation, OpenTelemetry tracing, and audit log generation.

---

## Alternatives Considered

### Alternative 1: Inline Prompts / Local Template Files in Plugins (Rejected)
Allow plugins and runtime modules to write inline prompts or manage local Jinja2 template files.
- **Rejected because**: Prevents platform-wide prompt versioning, security policy enforcement, token budget optimization, central audit logging, or prompt lineage tracing.

### Alternative 2: Coupling Prompt Management into the Agent Runtime (Rejected)
Embed prompt compilation and assembly directly inside the Agent Runtime module.
- **Rejected because**: Violates single responsibility principles. Non-agent modules (Workflow Engine tasks, Knowledge Base summarization pipelines, Tool formatters) also require prompt compilation without instantiating an autonomous agent loop.

---

## Consequences

### Positive Consequences

- **Centralized Governance & Versioning**: Full SemVer control over all prompt assets across all domain plugins.
- **Guaranteed Security & Compliance**: Automated safety policy enforcement, PII masking, and prompt injection scanning on every invocation.
- **Optimized LLM Spend & Context Window Usage**: Automated token budgeting, AST pruning, and semantic prompt compression prevent context overflows.
- **Immutable Lineage & Auditability**: Every LLM execution is cryptographically linked to its exact prompt template and context state.

### Trade-offs / Challenges

- **Additional System Layer**: Introduces new Layer 3 modules, Redis caches, and database schemas.
- **Compilation Overhead**: Adding template parsing and AST optimization adds fractional latency (mitigated by prompt caching).

---

## Repository Impact

### New Files to be Created

| Location | Layer | Description |
| :--- | :--- | :--- |
| `backend/core/ports/prompt.py` | Layer 0 | Core abstract interface contracts. |
| `backend/infrastructure/prompt/` | Layer 1 | Redis prompt caching & PostgreSQL manifest adapters. |
| `backend/prompt_runtime/` | Layer 3 | Subsystem modules (Registry, Compiler, Assembly, Policy, Optimizer). |
| `docs/architecture/prompt-runtime.md` | Docs | Full architecture specification. |
| `docs/adr/ADR-012-prompt-runtime.md` | Docs | This ADR document. |

---

## Related Documents

- Clean Architecture: `docs/architecture/clean-architecture.md`
- Platform Runtime: `docs/architecture/platform-runtime.md`
- Agent Runtime: `docs/architecture/agent-runtime.md`
- Tool Runtime: `docs/architecture/tool-runtime.md`
- Integration Runtime: `docs/architecture/integration-runtime.md`
- Prompt Spec: `docs/architecture/prompt-runtime.md`

---

*Accepted by Lead Architect — 2026-08-04*
