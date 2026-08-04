# ADR-011: Integration Runtime Architecture — Enterprise Integration Subsystem

**Title:** Integration Runtime Architecture — Enterprise Integration Subsystem  
**Status:** Accepted  
**Date:** 2026-08-04  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic Integration Runtime as the platform's authoritative enterprise integration subsystem, co-located in Platform Runtime (Layer 3), responsible for connecting NeuroFlow AI with external systems, databases, cloud services, message brokers, and protocols (including MCP) through a unified abstraction layer.

---

## Context

NeuroFlow AI is a production-grade modular AI Operating Platform. Following the completion of the Clean Architecture, Platform Runtime, Internal Event Bus, AI Memory Layer, Knowledge Base, Knowledge Graph, Workflow Engine, Agent Runtime, and Tool Runtime architectures, the next architectural milestone is external system integration.

Before this decision, external system interactions were handled ad hoc across plugins, tool execution handlers, and knowledge ingestors. Modules individually implemented custom REST clients, raw database connections, or specific SDK calls.

This fragmented approach introduced critical architectural risks:

- **Protocol & Library Coupling**: High-level modules were directly coupled to wire protocols, vendor SDKs, and transport mechanics.
- **Unmanaged Connection Infrastructure**: Lack of unified connection pooling caused socket exhaustion and unmanaged external resource consumption.
- **Security & Secret Exposure**: Credentials, API tokens, and private keys were managed inconsistently across plugin codebases, violating Zero Trust principles.
- **Missing Enterprise Governance & Multi-Tenancy**: External calls could not enforce tenant-scoped egress policies, rate limits, or audit logging.
- **Observability Gaps**: Outbound requests lacked standardized OpenTelemetry distributed tracing and metrics.

---

## Decision

**We will introduce a dedicated Integration Runtime as a reusable Platform Runtime (Layer 3) capability.**

The Integration Runtime is explicitly defined as:

> NeuroFlow AI's **enterprise integration subsystem**, responsible for governing all interactions between the platform and external systems, databases, cloud services, messaging fabrics, and legacy enterprise applications through a unified protocol abstraction layer.

The Integration Runtime is **not** an MCP implementation, **not** a REST client, and **not** an SDK wrapper. MCP is merely one of many supported protocols under an extensible Protocol Abstraction Layer.

All external communications initiated by any platform component (Tool Runtime, Knowledge Base, Workflow Engine, Event Bus) must execute through the Integration Runtime's `IIntegrationRuntime` port.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/integration-runtime.md`) establishes the following key structures:

### Layer Placement

The Integration Runtime resides in **Platform Runtime (Layer 3)** of the NeuroFlow AI Clean Architecture, co-located with the Agent Runtime, Tool Runtime, Workflow Engine, Knowledge Base, Knowledge Graph, and Memory Layer. Abstract contracts reside in Layer 0 (`backend/core/ports/integration.py`), and infrastructure adapters reside in Layer 1 (`backend/infrastructure/integration/`).

### Twenty Core Subsystems

1. **Connector Registry**: Multi-tier catalog storing, versioning, and indexing connector manifests.
2. **Connector Discovery Engine**: Dynamic semantic discovery and health-aware connector lookup.
3. **Auth & Secrets Manager**: Zero Trust credential resolution, OAuth flow automation, and Vault integration.
4. **Request/Response Validation Engine**: Schema verification and payload threat sanitization.
5. **Data Transformation Layer**: Payload format translation, codecs, and field-level mapping.
6. **Rate & Quota Limiter**: Per-tenant rate buckets and outbound egress quota enforcement.
7. **Circuit Breaker**: Connector state machine (Closed, Open, Half-Open) protecting external targets.
8. **Connection Pool Manager**: High-performance multiplexing, keepalive, and idle eviction.
9. **Protocol Abstraction Layer**: Unified router mapping normalized requests to concrete protocol adapters.
10. **Protocol Adapters**: Extensible adapters for REST, GraphQL, gRPC, WebSocket, MCP, SQL, NoSQL, Filesystems, Cloud Storage, and Message Brokers.
11. **Streaming Coordinator**: Support for SSE, gRPC streaming, and WebSocket streams with back-pressure.
12. **Retry Engine**: Exponential backoff with full jitter for transient failure recovery.
13. **Cache Engine**: Redis-backed idempotent integration response caching.
14. **Health Monitor**: Active probing and passive error-rate inspection.
15. **Observability & Audit Engine**: OpenTelemetry tracing, 24 exported metrics, and immutable audit logging.

---

## Alternatives Considered

### Alternative 1: Direct Integration per Plugin / Module (Rejected)
Allow plugins and platform tools to embed direct HTTP/gRPC/Database SDK calls.
- **Rejected because**: Creates severe protocol fragmentation, secret leakage risks, unmanaged socket pools, missing multi-tenant isolation, and complete lack of central governance.

### Alternative 2: Standardizing Exclusively on MCP (Model Context Protocol) (Rejected)
Use MCP as the sole protocol for all external integrations.
- **Rejected because**: While MCP is excellent for local and agent-centric tool interfaces, it is not suitable for high-throughput SQL database queries, binary gRPC streams, enterprise message broker consumption (Kafka/AMQP), or legacy enterprise SOAP/ASMX systems. MCP is treated as one supported protocol within a broader Protocol Abstraction Layer.

### Alternative 3: External API Gateway Dependency (Rejected)
Delegate all outbound routing and integration to an external cloud API Gateway or ESB.
- **Rejected because**: Introduces hard cloud vendor lock-in, increases network hops/latency, and fails to handle in-process local protocols (Stdio, IPC, embedded databases) required by plugins.

---

## Consequences

### Positive Consequences

- **Single Point of Egress Governance**: All outbound traffic obeys unified security, auth, rate limiting, and multi-tenant policies.
- **Protocol Independence**: Cognitive runtimes (Agent Runtime, Tool Runtime) remain completely agnostic of external wire formats.
- **Zero Trust Security**: Centralized Vault secret resolution, automated token rotation, and strict egress sandboxing.
- **High Throughput & Resilience**: Managed connection pools, circuit breakers, and exponential backoff retry policies guarantee platform stability.
- **Full Distributed Observability**: End-to-end trace propagation across external system boundaries.

### Trade-offs / Challenges

- **Expanded Subsystem Surface**: Introduces new Layer 3 modules, database tables, and Redis storage structures.
- **Latency Overhead**: Protocol abstraction and schema validation pipelines add fractional latency overhead (mitigated by connection pooling and in-memory caches).

---

## Repository Impact

### New Files to be Created

| Location | Layer | Description |
| :--- | :--- | :--- |
| `backend/core/ports/integration.py` | Layer 0 | Core abstract interface contracts. |
| `backend/infrastructure/integration/` | Layer 1 | Infrastructure drivers, Vault adapters, socket pools. |
| `backend/integration_runtime/` | Layer 3 | Subsystem modules (Registry, Discovery, Auth, Pooling, Adapters, Resilience). |
| `docs/architecture/integration-runtime.md` | Docs | Full architecture specification. |
| `docs/adr/ADR-011-integration-runtime.md` | Docs | This ADR document. |

---

## Related Documents

- Clean Architecture: `docs/architecture/clean-architecture.md`
- Platform Runtime: `docs/architecture/platform-runtime.md`
- Tool Runtime: `docs/architecture/tool-runtime.md`
- Agent Runtime: `docs/architecture/agent-runtime.md`
- Integration Spec: `docs/architecture/integration-runtime.md`

---

*Accepted by Lead Architect — 2026-08-04*
