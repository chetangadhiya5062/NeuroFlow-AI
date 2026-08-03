# ADR-008: Workflow Engine Architecture — Domain-Agnostic Orchestration Engine

**Title:** Workflow Engine Architecture — Domain-Agnostic Orchestration Engine  
**Status:** Accepted  
**Date:** 2026-08-03  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic workflow orchestration engine co-located in Platform Runtime (Layer 3) to coordinate multi-step AI execution across all platform capabilities and domain plugins.

---

## Context

NeuroFlow AI is a production-grade modular AI platform serving heterogeneous domain plugins across Telecom Intelligence, Cybersecurity, Healthcare, Finance, Cloud Operations, and Enterprise Knowledge domains.

Multi-step AI operations on the platform (e.g., retrieving context from the Knowledge Base, querying semantic subgraphs from the Knowledge Graph, executing autonomous reasoning loops via the Agent Runtime, persisting learnings into the Memory Layer, routing for human approval, and publishing results to the Event Bus) require complex, reliable orchestration.

Without a centralized, domain-agnostic orchestration engine, multi-step coordination would be embedded directly inside individual domain plugins. This produces fragmented execution models, lack of unified retry/compensation logic, inability to checkpoint long-running processes, absence of multi-tenant queue isolation, and vendor lock-in to external frameworks.

---

## Decision

**We will introduce a dedicated Workflow Engine as a reusable Platform Runtime (Layer 3) capability.**

The Workflow Engine is explicitly defined as:

> NeuroFlow AI's **domain-agnostic orchestration engine**, responsible for coordinating multi-step AI execution across the Knowledge Base, Knowledge Graph, Memory Layer, Agent Runtime, and external systems while remaining completely independent of any specific domain plugin.

The Workflow Engine is **not** Apache Airflow. It is **not** Temporal. It is **not** LangGraph. It is a first-class platform capability designed natively for NeuroFlow AI.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/workflow-engine.md`) establishes the following key structures:

### Layer Placement
The Workflow Engine resides in **Platform Runtime (Layer 3)** of the NeuroFlow AI Clean Architecture, co-located with the Knowledge Base, Knowledge Graph, AI Runtime, Agent Runtime, and Memory Layer.

### Eleven Core Subsystems
1. **Workflow Registry** — Definition storage, version catalog, audit log, active routing.
2. **Workflow Execution Planner** — DSL parsing, DAG construction, dead-node pruning, execution plan generation.
3. **Validation Pipeline** — Pre-flight 7-stage validation gate (schema, DAG, cycles, dependencies, permissions, plugins, variables).
4. **Execution Engine** — Task dispatch, sequential/parallel/conditional/dynamic/nested control.
5. **Task Executor Pool** — 13 platform task type executors (`KB_RETRIEVAL`, `GRAPH_TRAVERSAL`, `AGENT_EXECUTION`, `MEMORY_READ`, `MEMORY_WRITE`, `EVENT_PUBLISH`, `HUMAN_APPROVAL`, `CONDITION_BRANCH`, `PARALLEL_JOIN`, `PLUGIN_TASK`, `HTTP_CALL`, `TRANSFORM`, `DELAY`).
6. **State & Context Manager** — Workflow/task state machines, variable scopes (global, input, local, output, temp), context isolation.
7. **Checkpoint & Persistence Store** — Resumable execution snapshots (`ICheckpointStore`), definition, execution, state, and audit stores.
8. **Scheduler** — Cron, interval, and one-time time-based workflow triggering (`IWorkflowScheduler`).
9. **Compensation Engine** — Saga pattern reverse-dependency rollback orchestration for state-changing tasks.
10. **Observability & Audit Subsystem** — OpenTelemetry distributed tracing, 12 operational metrics, append-only compliance audit trail.
11. **Search & Dashboard Subsystem** — Discovery search index, real-time operational console, SLA breach monitoring.

### Key Architectural Capabilities
- **Declarative Workflow DSL**: YAML/JSON schema with template expressions (`{{...}}`).
- **Zero-Downtime Semantic Versioning**: Running workflow instances lock to their creation version; active definitions update seamlessly.
- **Saga Pattern Compensation**: Automatic reverse-order rollback for state-changing tasks on critical failure.
- **Durable Long-Running Workflows**: Checkpointed on suspension; zero thread/CPU consumption while suspended; resilient to platform restarts.
- **Human-in-the-Loop**: `HUMAN_APPROVAL` task type with role-based assignment, notification channels, and timeout escalation paths.
- **Six Execution Modes**: Synchronous, Asynchronous, Detached, Scheduled, Event-Driven, Streaming.
- **Nested Workflows & Templates**: Parent/child sub-workflow invocation and reusable parameterized templates.
- **Multi-Tenant Queue Isolation**: Per-tenant task queues (`ITaskQueue` port via Redis or Kafka), resource quotas, per-tenant checkpoint encryption.

### Core Interface Definitions (`backend/core/ports/workflow.py`)

| Interface | Layer | Purpose |
| :--- | :--- | :--- |
| `IWorkflowRegistry` | Layer 0 | Definition catalog, versioning, and registration contract. |
| `IWorkflowExecutor` | Layer 0 | Workflow instance execution and dispatch contract. |
| `ITaskExecutor` | Layer 0 | Extensible task type executor registration contract. |
| `ITaskQueue` | Layer 0 | Durable task queue abstraction contract. |
| `ICheckpointStore` | Layer 0 | Checkpoint persistence contract. |
| `IWorkflowStateManager` | Layer 0 | Workflow and task state machine persistence contract. |
| `IWorkflowScheduler` | Layer 0 | Schedule registration and firing contract. |

---

## Alternatives Considered

### Alternative 1: Embedded Plugin Orchestration (Rejected)
Allow each domain plugin to write its own custom Python code for multi-step execution.

**Rejected because:**
- Produces fragmented, inconsistent orchestration logic across plugins.
- Duplicate implementation of retry, compensation, checkpointing, and tracing in every plugin.
- No central observability or SLA monitoring.
- Breaks multi-tenant execution isolation.

### Alternative 2: Direct Coupling to Apache Airflow (Rejected)
Embed Apache Airflow as the platform's workflow engine.

**Rejected because:**
- Airflow is designed for batch data engineering pipelines, not real-time event-driven AI agent orchestration.
- High scheduling latency (seconds/minutes) unsuited for sub-second agent tool chains.
- Heavy infrastructure overhead; difficult to embed within a modular monolith clean architecture.

### Alternative 3: Direct Coupling to Temporal.io (Rejected)
Require Temporal server as a hard infrastructure dependency.

**Rejected because:**
- Introduces external framework lock-in and mandatory external service deployment.
- Violates NeuroFlow AI's port/adapter abstraction principle — platform execution logic should depend on Clean Architecture ports (`ITaskQueue`, `IWorkflowExecutor`), allowing backend adapters to use Redis, Kafka, or internal queues interchangeably.

---

## Consequences

### Positive Consequences
- **Unified Orchestration**: Single, production-grade engine coordinates all multi-step AI execution across all platform capabilities.
- **Resilience & Fault Tolerance**: Automatic retries, Saga pattern compensation, and checkpointed resumability eliminate partial failures.
- **Human Governance**: First-class human approval steps ensure safety and compliance before critical actions are executed.
- **Strict Clean Architecture Separation**: Domain plugins define workflows declaratively via DSL without touching engine internal execution logic.
- **Multi-Tenant Isolation**: Hard isolation at queue, worker, quota, and state storage boundaries.
- **Full Observability**: End-to-end OpenTelemetry distributed tracing and compliance audit logging.

### Negative Consequences / Trade-offs
- **Additional Subsystem Complexity**: 16 dedicated sub-modules in `backend/workflow_engine/` and 7 new core ports in `backend/core/ports/workflow.py`.
- **Infrastructure Dependencies**: Requires Redis/Kafka for task queues and PostgreSQL/Redis for state and definition persistence.

---

## Related Architecture Documents

| Document | Location |
| :--- | :--- |
| Clean Architecture & Layer Model | `docs/architecture/clean-architecture.md` |
| Backend Module Architecture | `docs/architecture/backend-modules.md` |
| Platform Runtime | `docs/architecture/platform-runtime.md` |
| Internal Event Bus | `docs/architecture/event-bus.md` |
| AI Memory Layer | `docs/architecture/memory-layer.md` |
| Knowledge Base | `docs/architecture/knowledge-base.md` |
| Knowledge Graph | `docs/architecture/knowledge-graph.md` |
| **Workflow Engine** *(This Decision)* | `docs/architecture/workflow-engine.md` |

---

*Accepted by Lead Architect — 2026-08-03*
