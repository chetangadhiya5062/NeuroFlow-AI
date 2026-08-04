# ADR-010: Tool Runtime Architecture — Production-Grade Tool Execution Environment

**Title:** Tool Runtime Architecture — Production-Grade Tool Execution Environment  
**Status:** Accepted  
**Date:** 2026-08-04  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic Tool Runtime as the platform's authoritative execution environment for every tool invocation, co-located in Platform Runtime (Layer 3), responsible for discovery, registration, validation, authorization, sandboxing, orchestration, execution, lifecycle management, observability, and governance of every tool used by the Agent Runtime, Workflow Engine, and all domain plugins.

---

## Context

NeuroFlow AI is a production-grade modular AI Operating Platform. By the time of this decision, the platform had established a complete foundation: Clean Architecture, Platform Runtime, Internal Event Bus, AI Memory Layer, Knowledge Base, Knowledge Graph, Workflow Engine, and Agent Runtime.

The Agent Runtime — the platform's intelligence orchestration engine — selects and invokes tools during every autonomous reasoning session. The Workflow Engine invokes tools as task type executors. Domain plugins register domain-specific tools. However, the mechanism that **actually executes** these tools — that validates them, authorizes them, sandboxes them, retries them, caches their results, rates them, and makes them fully observable — did not exist as a dedicated, authoritative platform subsystem.

Without a Tool Runtime, the following systemic gaps existed across the entire platform:

- **No unified execution contract**: Tool invocation logic was duplicated across the Agent Runtime's Tool Execution Engine, the Workflow Engine's task executors, and every domain plugin that implemented its own tool-calling logic. There was no single contract that all tool calls obeyed.
- **No platform-wide authorization**: Each caller enforced its own permission checks. A plugin tool could be invoked outside its declared scope without platform-level detection. There was no consistent 6-stage authorization gate applied uniformly across every invocation.
- **No input/output validation at the execution boundary**: Argument validation was ad hoc per-caller. LLM-generated tool arguments — which are structurally unreliable — were passed to executors without systematic JSON Schema enforcement, constraint checking, or injection sanitization.
- **No sandboxing or isolation**: Plugin tool executors ran with unconstrained access to the host process. A misbehaving plugin tool could consume unbounded memory, spawn arbitrary subprocesses, or make unconstrained outbound network calls.
- **No unified retry and timeout policy**: Each caller implemented its own retry logic independently. Retry behavior was inconsistent across tool categories. Fallback chaining did not exist.
- **No multi-tenant resource governance**: There was no mechanism to cap the execution resources (CPU, memory, invocations, cost) consumed by any individual tenant through tool usage.
- **No tool-level observability**: Tool invocation latency, failure rates, retry counts, cache behavior, and cost were not captured in a standardized, queryable form. The platform had no per-tool or per-tenant tool performance visibility.
- **No tool versioning or compatibility management**: Tool schema changes silently broke all callers. There was no semantic versioning, no deprecation lifecycle, and no grace period for callers to migrate.
- **No capability discovery**: The Agent Runtime's Planning Engine could not ask the platform "which tools are available to me for this goal?" in a ranked, structured, health-filtered way.
- **No streaming execution model**: Tools that produce incremental results were forced to buffer complete responses. Progressive, real-time tool output delivery was architecturally impossible.
- **No long-running tool lifecycle**: Tools that execute for minutes or hours blocked the calling agent's reasoning loop and consumed execution resources without lifecycle management, heartbeat monitoring, or structured cancellation.

---

## Decision

**We will introduce a dedicated Tool Runtime as a reusable Platform Runtime (Layer 3) capability.**

The Tool Runtime is explicitly defined as:

> NeuroFlow AI's **production-grade tool execution environment**, responsible for the complete lifecycle of every tool invocation on the platform — including discovery, registration, authorization, input/output validation, sandboxing, execution orchestration, retry management, streaming, long-running lifecycle management, result caching, rate limiting, resource quota enforcement, multi-tenant isolation, and full distributed observability.

The Tool Runtime is **not** a simple function-calling wrapper. It is **not** a tool catalog. It is **not** an HTTP proxy. It is **not** a plugin registry. It is a first-class platform capability designed natively for NeuroFlow AI's Clean Architecture, serving as the authoritative execution infrastructure for every tool on the platform.

**The single most important invariant**: every tool invocation on the platform — regardless of its origin (Agent Runtime, Workflow Engine, Scheduler, or direct API) — executes through the Tool Runtime's `IToolRuntime.invoke()` entry point. There is no alternative path.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/tool-runtime.md`) establishes the following key structures:

### Layer Placement

The Tool Runtime resides in **Platform Runtime (Layer 3)** of the NeuroFlow AI Clean Architecture, co-located with the Agent Runtime, Workflow Engine, Knowledge Base, Knowledge Graph, and Memory Layer. Abstract interface contracts reside at **Layer 0** (`backend/core/ports/tool_runtime.py`). Infrastructure adapters reside at **Layer 1** (`backend/infrastructure/tool_runtime/`).

### Seventeen Core Subsystems

1. **Tool Registry** — Three-tier storage: PostgreSQL primary store, Redis active index, vector store for discovery embeddings. Full CRUD lifecycle operations with version history and audit trail.
2. **Capability Discovery** — Goal-aligned semantic ANN search over tool description embeddings. Composite scoring: 50% semantic similarity + 20% success rate + 20% usefulness score + 10% latency. Health filtering, scope filtering, and deduplication.
3. **Tool Selection Pipeline** — 11-stage pipeline from LLM tool-call directive to authorized, cache-checked, execution-ready invocation request.
4. **Authorization Pipeline** — Mandatory 6-stage gate: identity validation → tenant boundary → scope enforcement → safety level gate → policy rule evaluation → argument-level authorization.
5. **Input Validation** — 5-stage pipeline: JSON Schema validation → constraint checking → input sanitization (injection detection) → type coercion → default value injection.
6. **Execution Context Assembly** — Constructs the complete runtime environment for each invocation: identity, observability context, runtime limits, validated arguments, and tenant-scoped platform service handles.
7. **Execution Engine** — Three execution modes: `SYNC` (blocking), `STREAMING` (chunk delivery), `ASYNC_POLL` (long-running background). Timeout deadline enforcement, concurrency management, and worker pool dispatch.
8. **Sandbox Controller** — Four sandbox profiles (LOW / MEDIUM / HIGH / CRITICAL) mapped by safety level. Enforces memory limits, CPU limits, network egress allowlists, and filesystem access policies via `IIsolatedExecutorBridge`.
9. **Executor Pool** — Platform built-in tool executor implementations for all 13 tool categories (KB, Graph, Memory, Workflow, Computation, Communication, External API, Database, File System, Code Execution, Agent, Plugin, Platform Admin).
10. **Retry Engine** — Exponential backoff with jitter. Configurable `max_attempts`, `initial_delay_ms`, `max_delay_ms`, and `retryable_error_types`. Fallback tool chain invocation on retry exhaustion.
11. **Output Validation** — 5-stage pipeline: null/empty check → output schema validation → content safety filter (PII detection and redaction, secret detection and blocking) → output size validation → result normalization to `ToolResult` schema.
12. **Result Assembler** — Constructs the standardized `ToolResult` with all metadata: `status`, `output`, `error`, `latency_ms`, `cost_usd`, `cached`, `trace_id`, `fallback_used`, `retry_count`, `redactions`.
13. **Streaming Coordinator** — Manages chunk delivery from streaming executors to callers. Applies per-chunk output validation and safety filtering. Enforces back-pressure when caller read rate < executor write rate. Supports SSE, gRPC server streaming, and WebSocket transports.
14. **Rate Limiter** — Four-level throttling: global platform → per-tenant per-category → per-tool global → per-caller session. Algorithms: Token Bucket (global, per-tool) and Sliding Window (per-tenant, per-caller).
15. **Tool Cache** — Redis-backed deterministic result cache for idempotent, cacheable tools. Cache key: `SHA-256(tool_id + version + normalized_arguments + tenant_id)`. TTL-based eviction with active invalidation on tool version change and dependency mutation events.
16. **Event Bus Integrator** — Publishes 15 tool lifecycle events; subscribes to 6 inbound event patterns including plugin load (triggers tool registration) and HITL decisions (resumes blocked invocations).
17. **Observability Engine** — OpenTelemetry trace hierarchy: `tool.invocation → tool.selection_pipeline → tool.authorization_pipeline → tool.input_validation → tool.execution → tool.output_validation`. 18 exported metrics. Structured JSON logs at DEBUG / INFO / WARN / ERROR / CRITICAL.

### Key Architectural Capabilities

- **Single Execution Contract**: `IToolRuntime.invoke()` is the one and only entry point for all tool calls across the entire platform. No tool execution bypasses this interface.
- **Tool Versioning with Compatibility Matrix**: Semantic versioning (MAJOR.MINOR.PATCH) with breaking-change-triggered MAJOR bumps. Deprecated versions remain callable through a configurable grace period. Compatibility matrix tracks which callers are bound to which tool versions.
- **Capability Discovery with Composite Scoring**: The Capability Discovery Engine combines semantic similarity, historical success rate, agent-reported usefulness, and invocation latency into a composite score that drives tool ranking for the Agent Runtime's Planning Engine.
- **Circuit Breaker per Tool**: Each tool maintains an independent circuit breaker state machine (CLOSED → OPEN → HALF_OPEN). An OPEN circuit prevents invocations against an unhealthy external dependency from accumulating timeouts and retries.
- **Sandbox Isolation via `IIsolatedExecutorBridge`**: The specific sandboxing technology (OS subprocess with cgroups, lightweight container, WASM sandbox) is abstracted behind a port. The Tool Runtime never depends on a specific isolation mechanism.
- **PII and Secret Protection**: Output validation detects and redacts PII in all tool outputs before results reach the calling agent's context. Secret detection hard-blocks results, preventing credential exfiltration through the tool pipeline.
- **Tool Performance Learning Loop**: After each agent session, the Tool Runtime writes `ToolPerformanceRecord` entries to Procedural Memory. Future agent sessions retrieve these records, enabling the Planning Engine to prioritize historically high-usefulness tools for similar goals.

### Core Interface Definitions (`backend/core/ports/tool_runtime.py`)

| Interface | Layer | Purpose |
| :--- | :--- | :--- |
| `IToolRuntime` | Layer 0 | Entry point for all tool invocations and registrations. |
| `IToolRegistry` | Layer 0 | Tool definition catalog, versioning, and lifecycle operations. |
| `IToolExecutor` | Layer 0 | Execution contract implemented by every tool executor class. |
| `IToolRegistryStore` | Layer 0 | Tool definition persistence (PostgreSQL). |
| `IToolIndexStore` | Layer 0 | Active tool index for O(1) lookup (Redis). |
| `IToolVectorStore` | Layer 0 | Tool embedding store for ANN discovery (vector DB). |
| `IToolCacheStore` | Layer 0 | Tool result cache (Redis). |
| `IQuotaStore` | Layer 0 | Tenant resource quota ledger (PostgreSQL). |
| `IToolAuditStore` | Layer 0 | Immutable tool invocation audit log. |
| `ILongRunningStore` | Layer 0 | Long-running invocation registry (Redis). |
| `IIsolatedExecutorBridge` | Layer 0 | Sandbox isolation abstraction (subprocess / container / WASM). |
| `IRateLimiter` | Layer 0 | Rate limiting abstraction (token bucket / sliding window). |

---

## Alternatives Considered

### Alternative 1: Tool Execution Logic Embedded in Each Caller (Rejected)

Allow each consumer of tools (Agent Runtime, Workflow Engine, each domain plugin) to implement its own tool invocation logic independently — its own validation, authorization, retry, sandboxing, and observability.

**Rejected because:**
- Produces an irreconcilable divergence in tool invocation semantics across the platform. Security guarantees (authorization, sandboxing, PII redaction) become caller-dependent and cannot be guaranteed uniformly.
- Every security fix, retry improvement, or observability enhancement must be replicated across all callers — a maintenance multiplier of 8+ as plugins grow.
- Breaks the Clean Architecture principle: execution infrastructure belongs at Layer 3, not scattered across Layer 2 plugins and Layer 3 platform consumers.
- No single authoritative observability point. Tool performance metrics would be scattered across agent session logs, workflow task logs, and plugin logs with no unified query surface.
- A plugin author forgetting to implement authorization enforcement could execute tools outside their declared scope without any platform-level detection or blocking.

### Alternative 2: Extend the Agent Runtime's Tool Execution Engine to Serve All Callers (Rejected)

Extend the Agent Runtime's existing Tool Execution Engine subsystem into a shared service that the Workflow Engine and plugins also call.

**Rejected because:**
- The Agent Runtime is the platform's intelligence orchestration engine. Its architectural scope is reasoning, planning, context assembly, reflection, and multi-agent collaboration — not tool execution infrastructure. Expanding it to be a shared tool execution service would violate its architectural boundary and introduce a circular dependency with the Workflow Engine.
- The Agent Runtime's Tool Execution Engine was designed to serve the Agent Runtime's reasoning loop. It lacks the scheduling model, long-running lifecycle management, streaming coordination, capability discovery, tenant quota enforcement, and circuit breaker features required for a platform-wide tool execution environment.
- The Agent Runtime is invoked by the Workflow Engine (as an `AGENT_EXECUTION` task). If the Workflow Engine were also a caller of a service inside the Agent Runtime, the dependency graph would contain a circular reference between two Layer 3 peers.

### Alternative 3: Use a Third-Party Tool-Calling Framework (e.g., LangChain Tools, Haystack Tools) (Rejected)

Adopt an external open-source tool-calling framework as the platform's tool execution layer.

**Rejected because:**
- No existing open-source framework provides the full production feature set required: platform-wide RBAC authorization, multi-tenant resource quotas, 4-level sandboxing, circuit breakers, tool versioning with compatibility matrices, structured capability discovery, and PII/secret output filtering.
- Embedding an external framework as the platform's authoritative tool execution environment introduces vendor lock-in. Tool schema formats, execution models, and retry policies would be dictated by the external framework's release cadence.
- External frameworks are not designed around NeuroFlow AI's Clean Architecture port/adapter model. Integrating them as a first-class platform layer would require wrapping them in ports — creating indirection that adds complexity without adding capability.
- The platform's multi-tenant, domain-agnostic design requires that tool governance (scopes, namespaces, quota dimensions) be platform-native concepts. No external framework models multi-tenancy at the tool execution level.

### Alternative 4: Serverless Function Dispatch (e.g., AWS Lambda, Cloud Functions) as Tool Execution Backend (Rejected)

Dispatch all tool invocations to serverless functions, using cloud function infrastructure as the tool execution environment.

**Rejected because:**
- Introduces a hard dependency on a specific cloud provider's infrastructure, violating the platform's vendor-agnostic, portable architecture.
- Cold-start latency (100ms–1s) is unacceptable for synchronous tool calls within an agent's real-time reasoning loop.
- The port/adapter model already provides the equivalent abstraction: `IIsolatedExecutorBridge` can be implemented by a serverless adapter without forcing the core Tool Runtime to depend on cloud-specific APIs.
- Multi-tenant quota enforcement, circuit breakers, and capability discovery index management require stateful platform-resident logic that does not map naturally to the stateless serverless execution model.

---

## Consequences

### Positive Consequences

- **Single Execution Path for All Tools**: Every tool invocation on the platform goes through exactly one code path. Security guarantees, authorization rules, and observability are enforced uniformly without exception.
- **Elimination of Cross-Cutting Duplication**: Retry logic, timeout enforcement, authorization checks, sandbox configuration, and metric emission — previously implemented inconsistently in multiple places — now exist in one place and are maintained once.
- **Production-Grade Safety**: The 6-stage Authorization Pipeline, 5-stage Input Validation, output PII redaction, secret blocking, and sandbox isolation provide layered defense-in-depth that no individual caller can replicate at equivalent quality.
- **Agent Reasoning Quality Improvement**: Capability Discovery with composite scoring enables the Planning Engine to recommend not just semantically relevant tools but tools with proven high success rates and low latency — improving planning quality and reducing tool call failures mid-reasoning.
- **Tool Performance Learning**: The retrospective `ToolPerformanceRecord` written to Procedural Memory creates a continuous improvement loop: agents learn which tools are most effective for specific goal contexts across sessions.
- **Multi-Tenant Fairness**: Per-tenant rate limits and resource quotas guarantee that no tenant's aggressive tool usage degrades the experience of other tenants on shared execution infrastructure.
- **Streaming and Long-Running Support**: The platform gains first-class support for progressive streaming tools (real-time data feeds, live analysis outputs) and long-running asynchronous tools (batch jobs, slow external APIs) without any caller-side orchestration complexity.
- **Full Distributed Observability**: 18 OpenTelemetry metrics, structured JSON logs, and distributed trace hierarchies provide complete visibility into every tool's latency, failure rate, cost, and usage patterns per tool, per tenant, and per caller type.
- **Clean Architecture Compliance**: All tool execution logic resides at Layer 3. All contracts are at Layer 0. Infrastructure adapters at Layer 1. Plugins at Layer 2 interact only through `IToolRuntime` port. The dependency rule is strictly observed throughout.

### Negative Consequences / Trade-offs

- **Significant New Platform Subsystem**: 20 dedicated sub-modules in `backend/tool_runtime/`, 12 new core ports in `backend/core/ports/tool_runtime.py`, and 9 infrastructure adapters in `backend/infrastructure/tool_runtime/` represent a substantial increase in platform scope and implementation surface.
- **Additional Storage Infrastructure**: Tool Runtime requires dedicated PostgreSQL tables (tool definitions, quota ledger, audit log), Redis namespaces (active index, result cache, long-running registry), and a vector store namespace (tool embeddings). These add operational, backup, and scaling responsibilities.
- **Refactoring of Existing Agent Runtime and Workflow Engine**: The Agent Runtime's Tool Execution Engine and the Workflow Engine's task executors must be updated to delegate through `IToolRuntime` rather than managing invocation pipelines internally. This is a one-time refactoring cost that eliminates long-term duplication.
- **Execution Overhead for Simple Tool Calls**: The full Tool Runtime pipeline (selection → authorization → validation → sandbox → execution → output validation) adds measurable overhead compared to a direct function call. For `LOW` safety level, stateless computation tools, this overhead is minimized by the in-memory Active Index and cache-first design. For `HIGH` and `CRITICAL` safety tools, the overhead is architecturally justified by the isolation and governance it provides.
- **Sandbox Technology Decision Deferred**: The `IIsolatedExecutorBridge` port abstracts the sandboxing technology, but a concrete technology decision (subprocess/cgroups vs. gVisor vs. WASM) must be made and an adapter implemented before `HIGH` and `CRITICAL` safety level tools can be activated in production.

---

## Repository Impact

### New Files

| Location | Layer | Count | Contents |
| :--- | :--- | :--- | :--- |
| `backend/core/ports/tool_runtime.py` | Layer 0 | 1 file | 12 abstract interface contracts. |
| `backend/infrastructure/tool_runtime/` | Layer 1 | 9 adapters | `postgres_tool_registry_store.py`, `redis_tool_index_store.py`, `redis_tool_cache_store.py`, `postgres_quota_store.py`, `postgres_tool_audit_store.py`, `redis_long_running_store.py`, `subprocess_executor_bridge.py`, `redis_rate_limiter.py`, `qdrant_tool_vector_store.py`. |
| `backend/tool_runtime/` | Layer 3 | 20 sub-modules | Full Tool Runtime implementation (see Architecture Summary above). |

### Modified Files

| File / Module | Change |
| :--- | :--- |
| `backend/core/ports/agent.py` | Replace standalone `IToolExecutor` with `IToolRuntime` port dependency. The Agent Runtime no longer owns tool execution; it delegates to the Tool Runtime. |
| `backend/agent_runtime/tools/` | Refactor Tool Execution Engine to invoke `IToolRuntime.invoke()` instead of managing its own validation, authorization, retry, and sandbox pipeline. |
| `backend/workflow_engine/tasks/` | Refactor `ToolExecutionTaskExecutor` and relevant platform task type executors to delegate through `IToolRuntime`. |
| `backend/plugins/*/` | Update all existing plugin tool registrations to use `context.tool_runtime.register_tool()` with the full Tool Definition schema. |

### Unchanged Files (Reference Only)

| Port File | Used By |
| :--- | :--- |
| `backend/core/ports/knowledge.py` | Injected as `IKnowledgeBaseClient` service handle into Execution Context. |
| `backend/core/ports/graph.py` | Injected as `IGraphClient` service handle. |
| `backend/core/ports/memory.py` | Injected as `IMemoryClient` service handle; also used for `ToolPerformanceRecord` writes. |
| `backend/core/ports/workflow.py` | Used by Workflow tool executor for `workflow_trigger` tool integration. |

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
| Workflow Engine | `docs/architecture/workflow-engine.md` |
| Agent Runtime | `docs/architecture/agent-runtime.md` |
| **Tool Runtime** *(This Decision)* | `docs/architecture/tool-runtime.md` |

## Related ADRs

| ADR | Decision |
| :--- | :--- |
| ADR-001 | Clean Architecture Adoption |
| ADR-002 | Modular Monolith with Plugin-First Architecture |
| ADR-003 | Platform Runtime Layer Introduction |
| ADR-004 | Internal Event Bus Architecture |
| ADR-005 | AI Memory Layer Architecture |
| ADR-006 | Enterprise Knowledge Base Architecture |
| ADR-007 | Knowledge Graph Architecture — Semantic Reasoning Layer |
| ADR-008 | Workflow Engine Architecture — Domain-Agnostic Orchestration Engine |
| ADR-009 | Agent Runtime Architecture — Intelligence Orchestration Engine |
| **ADR-010** *(This Decision)* | Tool Runtime Architecture — Production-Grade Tool Execution Environment |

---

## Future Extensions

| Extension | Description |
| :--- | :--- |
| **WASM Tool Sandbox** | Implement a WebAssembly-based `IIsolatedExecutorBridge` adapter for pure-compute tools, enabling near-native performance in a fully sandboxed execution environment without subprocess overhead. |
| **Tool Marketplace** | A governed discovery interface exposing the Tool Registry to authorized external developers, enabling third-party tool providers to contribute certified tools that appear in the platform's Capability Discovery index. |
| **Tool Composition Engine** | A declarative tool composition model allowing multiple primitive tools to be combined into a named composite tool with a single invocation interface. The composition is managed by the Tool Runtime, not the calling agent. |
| **Adaptive Rate Limiting** | Machine learning–driven rate limit tuning that automatically adjusts per-tenant and per-tool rate limits based on observed demand patterns, external dependency health, and platform capacity metrics. |
| **Tool A/B Testing** | Traffic splitting between two registered versions of the same tool, with automatic metric collection and statistical significance testing to determine which version performs better before full promotion. |
| **Cost Optimization Engine** | Automatic routing of tool invocations to lower-cost equivalent tools when the caller's cost budget is under pressure (e.g., route from a paid external API tool to a cached or on-platform equivalent). |
| **Tool Dependency Graph Visualization** | A platform admin capability that renders the full tool dependency graph (tool → platform_deps, external_deps, tool_deps) as an interactive visualization for architecture review and dependency risk assessment. |

---

*Accepted by Lead Architect — 2026-08-04*
