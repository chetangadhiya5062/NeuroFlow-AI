# ADR-004: Formalization of Internal Event Bus Architecture

- **Status**: Approved
- **Date**: 2026-08-01
- **Deciders**: Principal Software Architect, Lead Architect, Security Lead
- **Technical Story**: Establishing a domain-agnostic asynchronous messaging backbone for NeuroFlow AI.

---

## Context and Problem Statement

In the initial synchronous architecture of NeuroFlow AI, module actions (e.g., an autonomous agent finishing a task or a RAG document ingestion completing) directly invoked downstream observers (audit loggers, metric exporters, graph updaters, plugin hooks).

This direct-coupling model suffered from five critical flaws:
1. **High Coupling & Cascade Failures**: Failures in downstream observers failed the primary execution transaction.
2. **Poor Extensibility**: Adding new plugins required modifying core engine code to append new invocation calls.
3. **ASGI Event Loop Blocking**: Executing logging, telemetry, and plugin hooks synchronously inside main threads caused latency spikes.
4. **Testing Complexity**: Unit testing required mocking multiple unrelated downstream services.
5. **Microservice Barriers**: Direct method calls blocked future microservice extraction.

---

## Decision Drivers

1. **Decoupled Architecture**: Publishers emit facts without needing to know subscriber identities or signatures.
2. **Domain Agnosticism**: The Event Bus core must be 100% domain-agnostic (unaware of LLMs, RAG, Agents, or Telecom domain logic).
3. **Audit & Replayability**: Complete append-only historical event persistence for compliance, state recovery, and time-travel debugging.
4. **Enterprise Security**: Built-in payload encryption, digital signatures, tamper detection, and multi-tenant isolation.
5. **Clean Architecture Adherence**: Core ports in `core/ports/`, technical dispatch engines in `infrastructure/events/`.

---

## Considered Options

1. **Option 1: Retain Direct Synchronous Method Invocations**  
   *Rejected*. Causes tight coupling, cascade failures, and blocks future plugin/microservice scalability.
2. **Option 2: Embed Domain Logic directly into the Event Bus Engine**  
   *Rejected*. Violates single responsibility and prevents domain independence.
3. **Option 3: Adopt a Generic Event Bus with Event Store, Schema Registry, and Middleware Pipeline in `infrastructure/events/`**  
   *Selected*. Establishes a pure, domain-agnostic messaging substrate with complete event persistence and Clean Architecture alignment.
4. **Option 4: Create a new top-level backend folder `backend/event_bus/`**  
   *Rejected*. Causes top-level folder sprawl and violates Clean Architecture layer grouping (technical messaging drivers belong in `infrastructure/`).

---

## Decision Outcome

**Selected Option 3**: Adopt a **Generic, Domain-Agnostic Internal Event Bus** with an append-only **Event Store**, **Schema Registry**, and **Nine-Stage Middleware Pipeline**.

### Key Architectural Choices

1. **Layer Placement**:
   - Abstract ports (`IEventBus`, `IEventStore`, `ISchemaRegistry`, `BaseEvent`) placed in `backend/core/ports/` (Layer 0).
   - Concrete dispatchers, store persistence adapters, and pipeline middleware placed in `backend/infrastructure/events/` (Layer 1).
2. **Event Taxonomy & Topics**: Enforce hierarchical dot-notation (`neuroflow.workflow.started`, `telecom.pcap.analyzed`) across 10 formal event categories.
3. **Resiliency & Recovery**: Include Dead Letter Queue (DLQ), Exponential Backoff with Jitter retries, and Multi-Mode Event Replay (by Event ID, Topic, Time Range, Correlation ID).
4. **Priority Scheduling**: Enforce deterministic priority scheduling (`Priority 0` to `Priority N`) with 3000ms subscriber execution timeouts.

---

## Consequences

### Positive Consequences
- **Complete Decoupling**: Publishers emit events and immediately resume execution without waiting for subscribers.
- **Enhanced Extensibility**: Plugins and new platform features subscribe to existing event topics with zero changes to publishers.
- **Auditability & Replay**: The Event Store provides a permanent ledger for time-travel debugging and disaster recovery.
- **Security & Multi-Tenancy**: Built-in payload encryption, nonces, HMAC signatures, and tenant-scoped dispatching.
- **Microservice Readiness**: In-memory dispatcher can be swapped for Kafka, RabbitMQ, or Redis Streams without refactoring publisher code.

### Negative Consequences / Trade-offs
- **Eventual Consistency**: Asynchronous subscribers process events out-of-band; UI layers must handle eventual consistency (e.g., via WebSockets or polling).
- **Schema Management Overhead**: Requires managing JSON Schema versions in the Event Schema Registry to ensure backward/forward compatibility.

---

## Compliance & Enforcement

- **Documentation**: Comprehensive technical specification maintained in [`docs/architecture/event-bus.md`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/event-bus.md).
- **Automated Verification**: AST import linter rules in `tests/architecture/` enforce layer dependencies.

---

## References

- [Internal Event Bus Architecture Specification](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/event-bus.md)
- [Platform Runtime Architecture Specification](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/architecture/platform-runtime.md)
- [ADR-003: Platform Runtime Layer](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/docs/adr/ADR-003-platform-runtime.md)
