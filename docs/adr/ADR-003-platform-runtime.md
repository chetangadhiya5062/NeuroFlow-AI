# ADR-003: Formalization of Platform Runtime Logical Layer

- **Status**: Approved
- **Date**: 2026-08-01
- **Deciders**: Principal Software Architect, Lead Architect, Core Platform Team
- **Technical Story**: Clarification of Clean Architecture layer boundaries for AI engines (`ai`, `rag`, `agents`, `workflows`) in NeuroFlow AI.

---

## Context and Problem Statement

In initial architectural reviews of the NeuroFlow AI backend codebase, a classification ambiguity arose regarding core AI capabilities (`ai`, `rag`, `agents`, `workflows`). 

Under standard Clean Architecture templates, components interacting with external APIs or databases are frequently lumped into the **Infrastructure** layer. However:
- `ai` (LLM connectors & model routers)
- `rag` (semantic chunking, hybrid vector retrieval, context re-ranking)
- `agents` (autonomous reasoning loops, multi-step goal planners)
- `workflows` (DAG topology graph engine, state machine runners)

are **NOT technical infrastructure** (like Redis clients, Postgres pools, or S3 adapters), nor are they domain-specific **Application Use-Cases** (like `ExecuteTelecomDiagnosticUseCase`). 

Lumping cognitive algorithms into Infrastructure led to technical driver pollution and vendor lock-in. Conversely, placing raw LLM streaming or vector math inside Application Services bloated use-case code with non-domain mechanics.

---

## Decision Drivers

1. **Strict Clean Architecture Boundaries**: Technical infrastructure (drivers/adapters) must remain separate from cognitive algorithms (reasoning loops/chunking/DAG engines).
2. **Domain-Independent Intelligence Substrate**: Core AI capabilities must be reusable across both core platform services and external domain plugins (Telecom, Cybersecurity, Cloud, Finance).
3. **Developer Ergonomics**: Avoid deep nested import paths (e.g., `backend.platform_runtime.ai.engine`) that degrade developer velocity during early codebase development.
4. **Future Microservice & Compute Heterogeneity**: The architecture must allow independent scaling of GPU-heavy LLM inference, RAM-heavy vector search, and I/O-heavy DAG execution.

---

## Considered Options

1. **Option 1: Retain AI/RAG/Agents/Workflows inside Infrastructure**  
   *Rejected*. Causes infrastructure pollution by mixing low-level network/cache drivers with high-level cognitive reasoning logic.
2. **Option 2: Embed AI/RAG/Agents/Workflows directly into Application Services**  
   *Rejected*. Bloats use-case orchestrators with low-level prompt parsing, vector math, and token budgeting mechanics.
3. **Option 3: Introduce "Platform Runtime" as a Logical Architectural Layer while retaining flat physical directories (`backend/ai`, `backend/rag`, `backend/agents`, `backend/workflows`)**  
   *Selected*. Establishes clear layer boundaries in documentation and static AST linting without causing import path churn.
4. **Option 4: Introduce "Platform Runtime" as a Physical Directory (`backend/platform_runtime/`) immediately**  
   *Deferred*. Adds unnecessary path nesting during early phase development. Can be executed later if physical consolidation or microservice extraction becomes necessary.

---

## Decision Outcome

**Selected Option 3**: Introduce **Platform Runtime** as a formal **Logical Architectural Layer** (Layer 3) positioned between **Application Services** (Layer 4) and **Infrastructure / Core** (Layers 1 & 0).

Physical directory locations remain unchanged for developer ergonomics:
- `backend/ai/`
- `backend/rag/`
- `backend/agents/`
- `backend/workflows/`

### Architectural Layer Placement

```
Layer 5: Delivery & Ingress (backend/api)
Layer 4: Application Services (backend/services)
Layer 3: PLATFORM RUNTIME (backend/ai, backend/rag, backend/agents, backend/workflows) [NEW LOGICAL LAYER]
Layer 2: Extensions & Persistence (backend/plugins, backend/database)
Layer 1: Technical Infrastructure & Config (backend/infrastructure, backend/config)
Layer 0: Core Domain Model & Contracts (backend/core)
```

---

## Consequences

### Positive Consequences
- **Clear Architectural Boundaries**: Infrastructure is strictly limited to low-level technical drivers (Redis, Kafka, Postgres, S3).
- **Reusable Capability Substrate**: Application Services and Plugin SDKs interact with standard, domain-agnostic capability APIs (`ILLMEngine`, `IRAGEngine`, `IAgentRuntime`, `IWorkflowEngine`).
- **Zero Import Path Churn**: Developers continue importing from `backend.ai`, `backend.rag`, etc., maintaining high development velocity.
- **Microservice Readiness**: Any Platform Runtime engine can be extracted into a standalone service without changing code in `services` or `core`.

### Negative Consequences / Trade-offs
- **Virtual Boundary Enforcement**: Because Platform Runtime is a logical layer rather than a physical parent directory, layer compliance cannot rely solely on filesystem directory structure. It must be enforced via automated AST architectural linters (e.g., `import-linter` rules in `backend/tests/`).

---

## Compliance & Enforcement

- **Documentation**: Detailed architecture specification maintained in [`docs/architecture/platform-runtime.md`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/platform-runtime.md).
- **Automated Verification**: Import rules configured in `backend/tests/architecture/` will verify that `ai`, `rag`, `agents`, and `workflows` never import `services` or `api`.

---

## References

- [Platform Runtime Architecture Specification](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/platform-runtime.md)
- [NeuroFlow AI Architecture Review](file:///C:/Users/Hari/.gemini/antigravity-ide/brain/a4f5b938-8add-4806-950c-17082d6da110/neuroflow_ai_architecture_review.md)
