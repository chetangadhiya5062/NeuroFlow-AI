# ADR-007: Knowledge Graph Architecture — Semantic Reasoning Layer

**Title:** Knowledge Graph Architecture — Semantic Reasoning Layer  
**Status:** Accepted  
**Date:** 2026-08-03  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic semantic reasoning layer that models entities, relationships, ontologies, and explainable multi-hop reasoning pathways across all platform plugins.

---

## Context

NeuroFlow AI is a production-grade modular AI platform serving heterogeneous domain plugins across Telecom Intelligence, Cybersecurity, Healthcare, Finance, Cloud Operations, and Enterprise Knowledge domains.

Prior to this decision, the platform's knowledge management capabilities were limited to the enterprise Knowledge Base: a document lifecycle management system capable of ingesting, chunking, embedding, indexing, and retrieving knowledge fragments via hybrid vector + keyword search. While world-class for document retrieval, the Knowledge Base is fundamentally a **bag of isolated fragments** — it cannot model the structured semantic relationships between entities, cannot perform multi-hop inference, and cannot provide auditable reasoning chains to explain AI-generated conclusions.

The platform required a dedicated semantic layer that answers questions of the form *"How is entity A related to entity B?"*, *"Why did the platform conclude this?"*, and *"Trace all entities causally connected to this event"* — questions that are architecturally impossible to answer with a vector retrieval system alone.

---

## Decision

**We will introduce a dedicated Knowledge Graph as a reusable Platform Runtime (Layer 3) capability.**

The Knowledge Graph is explicitly defined as:

> The **semantic reasoning layer of NeuroFlow AI**, responsible for modeling entities, relationships, domain ontologies, knowledge provenance, and explainable multi-hop reasoning pathways across all platform plugins.

The Knowledge Graph is **not** a Vector Database. It is **not** a RAG implementation. It is **not** a replacement for the Knowledge Base. The Knowledge Base remains the primary document lifecycle management system. The Knowledge Graph is the **semantic intelligence layer built on top of** the Knowledge Base.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/knowledge-graph.md`) establishes the following key structures:

### Layer Placement
The Knowledge Graph resides in **Platform Runtime (Layer 3)** of the NeuroFlow AI Clean Architecture, co-located with the Knowledge Base, AI Runtime, Agent Runtime, Memory Layer, and Workflow Engine.

### Six Core Subsystems
1. **Entity Extraction Pipeline** — Five stages: NER → Coreference Resolution → Ontology Type Alignment → Attribute Extraction → Confidence Scoring.
2. **Relationship Extraction Pipeline** — Five stages: Dependency Parse → Relation Classification Model → Ontology Alignment → Rule-Based Enrichment → Confidence Scoring.
3. **Entity Resolution Engine** — Six stages: Exact Match → Alias → Fuzzy (Jaro-Winkler ≥ 0.92) → Embedding (cosine ≥ 0.95) → Attribute Cross-Validation → Manual Review Queue.
4. **Graph Store** — All storage delegated via `IGraphStore` port (Neo4j, Amazon Neptune adapters).
5. **Traversal Engine** — BFS, DFS, Shortest Path, Subgraph Extraction, Property Path, Time-Aware Traversal strategies.
6. **Reasoning Engine** — Confidence propagation with hop decay, evidence citation, Graph-RAG context assembly.

### Graph Versioning Strategy
Entity nodes and relationship edges carry integer `version` fields. Ontology layers are versioned under a semantic scheme (`MAJOR.MINOR` for Core Ontology). Schema evolution follows a four-phase migration strategy: Dual-Write → Batch Migration → Validation → Old Label Retirement. Backward compatibility is guaranteed during the dual-write period.

### Graph Query Engine (Vendor-Neutral Abstraction)
The platform depends on `IGraphQuery` — a vendor-neutral query abstraction port — rather than any graph database's native query syntax. `GraphQuerySpec` (a typed platform-native DSL) is transpiled to Cypher (Neo4j), Gremlin (Neptune/CosmosDB), or SPARQL at the infrastructure adapter layer. An ISO GQL adapter slot is reserved for future standards alignment.

### Confidence Propagation
Path confidence is computed as:
$$C_{\text{path}} = \left(\prod_{i} C_{\text{node}_i} \times \prod_{j} C_{\text{edge}_j}\right) \times \delta^{n}$$
Where $\delta = 0.95$ is the hop decay factor and $n$ is the hop count. Reasoning paths below the configurable minimum confidence threshold (default: 0.40) are excluded from LLM context assembly.

### Temporal Knowledge Graph
Every entity and relationship carries `valid_from`, `valid_until`, `recorded_at`, and `temporal_precision` temporal metadata fields. Standard traversal returns only currently valid entities. Time-travel queries return the graph state at any specified `as_of` timestamp. Historical reasoning applies temporal confidence decay: $C_{\text{temporal}} = C_{\text{path}} \times e^{-\lambda \Delta t}$.

### Graph Validation Pipeline
A seven-stage validation pipeline gates all entity and relationship candidates before graph store commitment: Ontology Validation, Schema Validation, Invalid Edge Detection, Cycle Detection, Broken Reference Detection, Duplicate Relation Detection, Entity Consistency Validation.

### Graph Cache Architecture
A four-tier Redis-backed Graph Cache Layer sits between the Traversal Engine and graph store: Hot Entity Cache (30-min TTL), Traversal Cache (15-min TTL), Subgraph Cache (10-min TTL), Query Cache (5-min TTL). Per-tenant namespace isolation. Cache warming on platform startup.

### Knowledge Graph Governance
A nine-state governance lifecycle (Draft → PendingReview → Approved → Active → UnderAmendment → Deprecated → LegalHold → Deleted) with a confidence-based auto-approval threshold (≥ 0.90), four stewardship roles (Platform Ontology Steward, Domain Steward, Tenant Data Steward, Compliance Officer), and immutable audit trail on every state transition.

### Distributed Graph Scaling
Graph partitioned along tenant and namespace dimensions. Horizontal sharding with automatic rebalancing. Read replicas serve all traversal queries (read/write separation). Write Coordinator manages cross-shard consistency for entity merge operations. Distributed traversal fan-out for cross-namespace queries.

### Port Definitions (Layer 0 — Core)

| Interface | Location | Purpose |
| :--- | :--- | :--- |
| `IGraphStore` | `backend/core/ports/graph.py` | Graph database storage port (upsert, traverse, deprecate, delete). |
| `IGraphQuery` | `backend/core/ports/graph.py` | Vendor-neutral query abstraction; transpiles `GraphQuerySpec` to Cypher/Gremlin/GQL. |
| `IEntityExtractor` | `backend/core/ports/graph.py` | Entity extraction model registry port. |
| `IRelationExtractor` | `backend/core/ports/graph.py` | Relation extraction model registry port. |
| `IReasoningEngine` | `backend/core/ports/graph.py` | Reasoning path serialization and confidence propagation port. |
| `IOntologyRegistry` | `backend/core/ports/graph.py` | Ontology type and extraction rule registry port. |

### Graph-RAG Integration
Entity recognition on incoming queries → seed entity lookup → N-hop subgraph extraction → serialized reasoning paths merged with standard Knowledge Base vector retrieval results → single LLM context block containing both text chunks and graph reasoning paths.

---

## Alternatives Considered

### Alternative 1: Vector Database as Semantic Layer (Rejected)
Use the vector database directly for entity relationship modeling by encoding entity pairs as embedding vectors.

**Rejected because:**
- Vector databases store dense embeddings for similarity search — they cannot model typed, directed, weighted relationships between entities.
- No traversal capability: a vector database cannot answer "what is two hops from entity A via a CAUSES relation?".
- No ontology or type system. All entity semantic structure is lost in the embedding.
- No provenance tracing at the entity-relation level.

### Alternative 2: Relational Database Graph Simulation (Rejected)
Model entities as rows and relationships as foreign key joins in the existing relational database.

**Rejected because:**
- Relational databases are architecturally unsuited for variable-depth graph traversal. Multi-hop JOIN chains become exponentially expensive and unmanageable at scale.
- No native graph traversal algorithms (BFS, DFS, shortest path).
- Schema rigidity prevents flexible ontology extension by plugins.
- No support for property-typed, weighted, directed edges.

### Alternative 3: Plugin-Local Entity Stores (Rejected)
Each domain plugin maintains its own local entity registry.

**Rejected because:**
- Zero cross-domain entity resolution or relationship modeling.
- The same physical entity (e.g., "Nokia 5G Base Station Site 44") could exist as unrelated records in Telecom and Cybersecurity plugins simultaneously.
- No cross-plugin reasoning or shared provenance.
- Multiplicative maintenance cost as plugin count grows.

### Alternative 4: Third-Party Knowledge Graph SaaS (Rejected)
Integrate a commercial knowledge graph platform as the platform's semantic layer.

**Rejected because:**
- Violates the platform's vendor-agnostic abstraction strategy.
- External SaaS dependency introduces availability risk and data residency concerns.
- Cannot integrate natively with the Internal Event Bus, Memory Layer, or Agent Runtime.
- No support for NeuroFlow AI's plugin ontology extension model.

---

## Consequences

### Positive Consequences

- **Multi-hop semantic reasoning** across all platform plugins and all knowledge sources — a capability architecturally impossible before this decision.
- **Explainable AI** — every AI conclusion is backed by a traversable, auditable reasoning path with evidence citations and confidence scores.
- **Entity deduplication at scale** — the six-stage Entity Resolution Engine ensures that the same real-world entity is consolidated into a single canonical node regardless of how many documents reference it.
- **Vendor-agnostic graph storage and querying** — `IGraphStore` and `IGraphQuery` ports ensure full graph database vendor flexibility.
- **Temporal reasoning** — `valid_from`/`valid_until` fields and time-travel queries enable point-in-time graph reconstruction for historical analysis and compliance.
- **Graph-RAG** — structured graph reasoning paths combined with Knowledge Base vector retrieval significantly enrich LLM context assembly beyond what vector retrieval alone can achieve.
- **Production-grade governance** — nine-state governance lifecycle with auto-approval, steward review, legal hold, and immutable audit trail.

### Negative Consequences / Trade-offs

- **Significant new platform subsystem** — 14 Knowledge Graph sub-modules, three new infrastructure adapters, and six new core ports represent a substantial increase in platform complexity.
- **Graph database operational dependency** — Neo4j or Amazon Neptune becomes a required infrastructure component, adding operational management, backup, and monitoring overhead.
- **Redis Graph Cache dependency** — A dedicated Redis namespace is required for the four-tier Graph Cache Layer.
- **Entity extraction quality is bounded by NER and RE model quality** — garbage-in-garbage-out: low-quality extraction models produce low-quality graph content. Governance stewardship is required to maintain graph accuracy.
- **Incremental extraction latency** — There is measurable lag between a Knowledge Base document being indexed and its entities appearing in the Knowledge Graph. The `neuroflow_kg_sync_lag_seconds` metric must be monitored against SLO.

---

## Compliance Notes

- Entities classified with `RESTRICTED` or `CONFIDENTIAL` access levels are traversal-restricted to `ROLE_RESTRICTED` or `ADMIN_ONLY` requester roles.
- GDPR hard-deletion requests must invoke the complete deletion path: removal of all entity nodes, all associated relationship edges, all cache entries, all provenance records, and all governance audit entries for the requested entity scope.
- **Legal Hold** state prevents any deletion or deprecation operations on affected entities regardless of TTL policy or governance lifecycle state.
- The immutable governance audit trail must be retained for the full duration of the tenant's data retention policy.

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
| **Knowledge Graph** *(This Decision)* | `docs/architecture/knowledge-graph.md` |

## Related ADRs

| ADR | Decision |
| :--- | :--- |
| ADR-001 | Clean Architecture Adoption |
| ADR-002 | Modular Monolith with Plugin-First Architecture |
| ADR-003 | Platform Runtime Layer Introduction |
| ADR-004 | Internal Event Bus Architecture |
| ADR-005 | AI Memory Layer Architecture |
| ADR-006 | Enterprise Knowledge Base Architecture |
| **ADR-007** *(This Decision)* | Knowledge Graph Architecture — Semantic Reasoning Layer |

---

*Accepted by Lead Architect — 2026-08-03*
