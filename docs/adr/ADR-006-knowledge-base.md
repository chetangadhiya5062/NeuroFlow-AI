# ADR-006: Enterprise Knowledge Base Architecture

**Title:** Enterprise Knowledge Base Architecture  
**Status:** Accepted  
**Date:** 2026-08-03  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic enterprise knowledge management subsystem as a reusable Platform Runtime capability.

---

## Context

NeuroFlow AI is a production-grade modular AI platform serving heterogeneous domain plugins (Telecom Intelligence, Cybersecurity, Healthcare, Finance, Cloud, Enterprise Knowledge). Each domain plugin requires access to large volumes of structured enterprise knowledge to ground AI inference, enable Retrieval-Augmented Generation (RAG), and support agent-driven knowledge queries.

Prior to this decision, no centralized knowledge management system existed. Each plugin was responsible for independently sourcing, loading, and indexing its own knowledge corpus, producing the following systemic problems:

- **Duplicated infrastructure logic** across plugins (document loaders, custom vector indices, retrieval pipelines).
- **Irreconcilable indexing strategies** between plugins, preventing cross-domain knowledge retrieval.
- **No access control or multi-tenant isolation** at the knowledge asset level.
- **No document lifecycle governance** — no versioning, archival, deprecation, or compliance hold capability.
- **No quality guarantees** over ingested content, risking garbage-in-garbage-out retrieval degradation.
- **No lineage or provenance tracing** from source document to LLM output.

The platform required a centralized, domain-agnostic enterprise knowledge management subsystem that governs the complete lifecycle of knowledge assets and exposes standardized interfaces to all platform consumers.

---

## Decision

**We will introduce a dedicated Enterprise Knowledge Base as a reusable Platform Runtime (Layer 3) capability.**

The Knowledge Base is explicitly defined as:

> The **complete lifecycle management system for enterprise knowledge**, governing how documents are ingested, parsed, structured, indexed, versioned, retrieved, updated, archived, and deleted.

The Knowledge Base is **not** a Vector Database. It is **not** a RAG implementation. The underlying Vector Database and RAG retrieval engine are technical subsystems invoked by the Knowledge Base.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/knowledge-base.md`) establishes the following key structures:

### Layer Placement
The Knowledge Base resides in **Platform Runtime (Layer 3)** of the NeuroFlow AI Clean Architecture, co-located with the AI Runtime, Agent Runtime, Memory Layer, and Workflow Engine.

### Five Core Subsystems
1. **Ingestion Pipeline** — Nine-stage pipeline: Upload → Validation → Parse → Quality Validation → Chunk → Embed → Index → Catalogue → Event Publish.
2. **Knowledge Store** — Multi-tier storage: Vector index (via IVectorStore port), Metadata catalogue (relational), Raw document store (blob storage).
3. **Retrieval Engine** — Hybrid retrieval: Dense HNSW ANN vector search + BM25 sparse keyword search merged via Reciprocal Rank Fusion (RRF), followed by cross-encoder re-ranking.
4. **Lifecycle Manager** — Versioning, freshness synchronization, TTL policy enforcement, incremental delta indexing, and archival.
5. **Access Control Gate** — RBAC enforcement, multi-tenant isolation, plugin namespace sandboxing.

### Source Connector Framework
A dedicated **Source Connector Framework** with a **Sync Scheduler** enables continuous synchronization from nine enterprise source types: Local Filesystem, Git Repositories, SharePoint/OneDrive, Confluence/Notion, S3/Azure Blob/GCS, Google Drive, REST APIs, Relational Databases (CDC), and Event Streams (Kafka/NATS).

### Knowledge Quality Validation Pipeline
A six-stage **Quality Validation Pipeline** gates all content before indexing: Duplicate Detection (SHA-256 + MinHash), OCR Quality Assessment, Language Detection, Metadata Completeness Check, Corrupted Document Detection, and Parser Confidence Scoring.

### Incremental (Delta) Indexing
Document updates trigger chunk-level diff computation. Only **Added**, **Modified**, and **Deleted** chunks are re-processed. Unchanged chunks retain existing embeddings. Embedding cost and indexing latency are proportional to change size, not total document size.

### Hierarchical Collection Model
Knowledge is organized into a four-level hierarchy: `Collection → Namespace → Document → Chunk`, enabling domain-scoped isolation (e.g., `kb_tenant-enterprise-01 / telecom / 3GPP_TS_28.552_v17.pdf / chunk_022`).

### Extended Enterprise Governance Metadata
Every document carries a governance metadata envelope including: `owner`, `department`, `confidentiality_level`, `compliance_tags`, `review_status`, `trust_score`, `retention_class`, `created_by`, `updated_by`, and `checksum_sha256`.

### Knowledge Governance Lifecycle
A seven-state governance lifecycle governs editorial approval and compliance: `Draft → Under Review → Approved → Published → Deprecated → Archived → Deleted`, with an out-of-band `Legal Hold` state that freezes documents under compliance instructions.

### Retrieval Strategy Registry
Seven retrieval strategies are registered via the `IRetrievalStrategy` port: `HYBRID_RETRIEVAL` (default), `DENSE_RETRIEVAL`, `SPARSE_RETRIEVAL`, `METADATA_RETRIEVAL`, `GRAPH_RETRIEVAL` (future), `PLUGIN_RETRIEVAL`, and `FEDERATED_RETRIEVAL` (future).

### Knowledge Cache Layer
A three-tier Redis-backed **Knowledge Cache Layer** sits between the Retrieval Engine and LLM context assembly: Semantic Cache (query embedding hash keyed), Hot Document Cache (top-K chunk text), and Redis acceleration with per-tenant namespace isolation.

### Knowledge Lineage & Provenance
Every retrieval response carries a structured lineage payload tracing the full chain: `Original Source → Document Version → Chunk → Embedding → Retrieved Context → LLM Response`, enabling explainability, debugging, and compliance auditing.

### Port Definitions (Layer 0 — Core)
| Interface | Location | Purpose |
| :--- | :--- | :--- |
| `IKnowledgeBase` | `backend/core/ports/knowledge.py` | Primary Knowledge Base domain port. |
| `IDocumentParser` | `backend/core/ports/knowledge.py` | Parser plugin registration port. |
| `IChunkingStrategy` | `backend/core/ports/knowledge.py` | Chunking strategy registry port. |
| `IEmbeddingProvider` | `backend/core/ports/embedding.py` | Embedding provider abstraction port. |
| `IVectorStore` | `backend/core/ports/vector_store.py` | Vector store backend abstraction port. |
| `IRetrievalStrategy` | `backend/core/ports/knowledge.py` | Retrieval strategy registry port. |

---

## Alternatives Considered

### Alternative 1: Plugin-Local Knowledge Stores (Rejected)
Each domain plugin manages its own isolated vector index and document loader.

**Rejected because:**
- Zero cross-domain knowledge reuse.
- N independent ingestion pipelines with no quality guarantees.
- No tenant-level isolation or governance.
- Multiplicative infrastructure cost as plugins scale.

### Alternative 2: Adopt a Third-Party Knowledge Management SaaS (Rejected)
Integrate a commercial knowledge platform (e.g., Notion AI, Guru, Confluence) as the platform knowledge store.

**Rejected because:**
- Violates the platform's vendor-agnostic abstraction strategy.
- External SaaS dependency introduces availability risk and data residency concerns.
- No native integration with NeuroFlow AI's Event Bus, Memory Layer, or Agent Runtime.
- Cannot be customized to support plugin-defined chunking strategies or domain-specific parsers.

### Alternative 3: Vector Database as Knowledge Base (Rejected)
Treat the vector database (Qdrant, Milvus) directly as the Knowledge Base, ingesting documents directly from plugins.

**Rejected because:**
- A Vector Database provides only ANN similarity search; it has no document lifecycle management capability.
- No versioning, archival, governance lifecycle, quality validation, or lineage tracing.
- Tight vendor coupling — switching vector stores would require changes throughout all plugins.
- No access control or multi-tenant isolation at the application semantic level.

---

## Consequences

### Positive Consequences

- **Unified enterprise knowledge management** across all current and future domain plugins.
- **Vendor-agnostic design** via `IVectorStore`, `IEmbeddingProvider`, and `IRetrievalStrategy` ports — full backend flexibility.
- **Production-grade quality assurance** through the six-stage Quality Validation Pipeline.
- **Cost-efficient incremental updates** via Delta Indexing — embedding cost proportional to document delta, not total document size.
- **Full compliance readiness** — document governance lifecycle with Legal Hold, GDPR-compliant hard deletion, retention class enforcement.
- **Complete observability** — nine OpenTelemetry-compatible metrics covering ingestion, quality failures, retrieval, cache hit ratios, and delta indexing ratios.
- **Future-ready for Knowledge Graph** — Knowledge Base documents serve as the primary entity extraction source for the future Knowledge Graph engine and `GRAPH_RETRIEVAL` strategy.

### Negative Consequences / Trade-offs

- **Increased platform complexity** — The Knowledge Base introduces a significant new subsystem that requires dedicated operational monitoring, SRE runbooks, and connector credential management.
- **Connector maintenance overhead** — Nine enterprise source connector types require ongoing authentication credential rotation and API compatibility maintenance.
- **Redis operational dependency** — The Knowledge Cache Layer introduces Redis as a required infrastructure dependency for the retrieval path.
- **Quality validation latency** — The six-stage Quality Validation Pipeline adds measurable latency to the ingestion path for large documents. Asynchronous ingestion mitigates user-facing impact.

---

## Compliance Notes

- Documents classified as `RESTRICTED` or `CONFIDENTIAL` must be stored in tenant-scoped isolated vector collections with `ADMIN_ONLY` or `ROLE_RESTRICTED` access scopes.
- GDPR hard-deletion requests must invoke the complete deletion path: removal of all chunk embeddings, metadata catalogue rows, blob storage objects, and Redis cache entries.
- Legal Hold state prevents any deletion or archival operations regardless of TTL or retention class policy.

---

## Related Architecture Documents

| Document | Location |
| :--- | :--- |
| Clean Architecture & Layer Model | `docs/architecture/clean-architecture.md` |
| Backend Module Architecture | `docs/architecture/backend-modules.md` |
| Platform Runtime | `docs/architecture/platform-runtime.md` |
| Internal Event Bus | `docs/architecture/event-bus.md` |
| AI Memory Layer | `docs/architecture/memory-layer.md` |
| **Knowledge Base** *(This Decision)* | `docs/architecture/knowledge-base.md` |

## Related ADRs

| ADR | Decision |
| :--- | :--- |
| ADR-001 | Clean Architecture Adoption |
| ADR-002 | Modular Monolith with Plugin-First Architecture |
| ADR-003 | Platform Runtime Layer Introduction |
| ADR-004 | Internal Event Bus Architecture |
| ADR-005 | AI Memory Layer Architecture |
| **ADR-006** *(This Decision)* | Enterprise Knowledge Base Architecture |

---

*Accepted by Lead Architect — 2026-08-03*
