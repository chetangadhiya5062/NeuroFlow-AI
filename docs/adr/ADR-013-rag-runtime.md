# ADR-013: RAG Runtime Architecture — Retrieval Intelligence Subsystem

**Title:** RAG Runtime Architecture — Retrieval Intelligence Subsystem  
**Status:** Accepted  
**Date:** 2026-08-04  
**Deciders:** Principal Software Architect, Lead Architect  
**Technical Story:** Establish a production-grade, domain-agnostic RAG Runtime as the platform's authoritative retrieval intelligence subsystem, co-located in Platform Runtime (Layer 3), responsible for query analysis, multi-source hybrid retrieval planning, cross-source fusion, re-ranking, source credibility scoring, citation generation, and context packaging.

---

## Context

NeuroFlow AI is a production-grade modular AI Operating Platform. Following the completion of Clean Architecture, Platform Runtime, Internal Event Bus, AI Memory Layer, Knowledge Base, Knowledge Graph, Workflow Engine, Agent Runtime, Tool Runtime, Integration Runtime, and Prompt Runtime architectures, the next architectural milestone is retrieval intelligence.

Before this decision, retrieval was fragmented across individual platform layers (Knowledge Base vector search, Knowledge Graph traversals, Memory Layer lookups). Subsystems executed isolated searches without query intent classification, multi-source fusion, cross-encoder re-ranking, token budget compression, or verifiable citation generation.

This fragmented approach introduced critical architectural liabilities:

- **Low Precision & Recall**: Naive vector similarity searches missed exact keywords, serial numbers, or complex entity relationships.
- **Single-Source Myopia**: Inability to seamlessly merge vector, keyword, graph, and memory retrieval into a unified context payload.
- **Hallucinated & Unverifiable Context**: Lack of chunk-level cryptographic attribution hashes and verifiable source citations.
- **Context Window Flooding**: Unfiltered search results polluted LLM prompt contexts, exceeding token budgets and degrading reasoning quality.

---

## Decision

**We will introduce a dedicated RAG Runtime as a reusable Platform Runtime (Layer 3) capability.**

The RAG Runtime is explicitly defined as:

> NeuroFlow AI's **retrieval intelligence subsystem**, responsible for query analysis, multi-source hybrid retrieval planning, cross-source fusion, re-ranking, source credibility scoring, citation generation, and context packaging across all platform modules and domain plugins.

The RAG Runtime is **not** a vector database, **not** an embedding model, and **not** the Knowledge Base.

All retrieval operations within NeuroFlow AI must pass through the RAG Runtime via the `IRagRuntime` port.

---

## Architecture Summary

The approved architecture (documented in `docs/architecture/rag-runtime.md`) establishes the following key structures:

### Layer Placement

The RAG Runtime resides in **Platform Runtime (Layer 3)** at `backend/rag_runtime/`, co-located with the Agent Runtime, Tool Runtime, Workflow Engine, Prompt Runtime, Knowledge Base, Knowledge Graph, and Memory Layer. Abstract contracts reside in Layer 0 (`backend/core/ports/rag.py`), and storage/embedding adapters reside in Layer 1 (`backend/infrastructure/rag/`).

### Ten Core Subsystems

1. **Query Analysis Engine**: Intent classification, query rewriting, and HyDE expansion.
2. **Retrieval Planner**: Builds parallel execution DAGs across multi-source retrievers.
3. **Retriever Registry**: Manages vector, keyword, graph, memory, and external retriever modules.
4. **Hybrid Fusion Engine**: Merges candidate sets using Reciprocal Rank Fusion (RRF).
5. **Deduplication Engine**: Content hash (SHA-256) and semantic MinHash deduplication.
6. **Re-ranking Engine**: Cross-encoder neural re-scoring (Cohere Rerank, BGE-Reranker).
7. **Validation & Credibility Gate**: Freshness checks and source trust score auditing.
8. **Citation Generator**: Generates cryptographic chunk attributions and verifiable source links.
9. **Context Packager**: Token budget-aware AST context assembly and compression.
10. **Observability Engine**: OpenTelemetry tracing, 18 metrics, and structured log generation.

---

## Alternatives Considered

### Alternative 1: Direct Subsystem Retrieval Calls (Rejected)
Allow Prompt Runtime and Agent Runtime to execute direct vector queries against Knowledge Base or graph queries against Knowledge Graph.
- **Rejected because**: Prevents multi-source hybrid fusion, cross-encoder re-ranking, query expansion, uniform citation generation, and token budget compression.

### Alternative 2: Coupling RAG into the Knowledge Base Subsystem (Rejected)
Embed the RAG Runtime pipeline directly inside the Knowledge Base module.
- **Rejected because**: Violates Clean Architecture separation of concerns. The Knowledge Base is responsible for document ingestion, parsing, chunking, and storage. The RAG Runtime is responsible for cross-subsystem retrieval intelligence across KB, KG, Memory Layer, and Integration Runtime connectors.

---

## Consequences

### Positive Consequences

- **Superior Retrieval Precision & Recall**: Hybrid search combining Vector (HNSW), Keyword (BM25), Knowledge Graph (Triples), and Memory with Cross-Encoder re-ranking.
- **Verifiable Citation Lineage**: Every context chunk carries a cryptographic attribution hash and source URI.
- **Token Budget Protection**: Context assembly respects prompt token boundaries via dynamic pruning and semantic compression.
- **Multi-Source Unification**: Single `IRagRuntime` interface orchestrates local vector stores, graph databases, memory layers, and remote enterprise endpoints.

### Trade-offs / Challenges

- **Additional System Layer**: Introduces new Layer 3 modules, re-ranker model infrastructure, and fusion logic.
- **Latency Budget Management**: Running query expansion and cross-encoder re-ranking adds latency (mitigated by parallel execution and caching).

---

## Repository Impact

### New Files to be Created

| Location | Layer | Description |
| :--- | :--- | :--- |
| `backend/core/ports/rag.py` | Layer 0 | Core abstract interface contracts. |
| `backend/infrastructure/rag/` | Layer 1 | Vector store, embedding provider, and re-ranker adapters. |
| `backend/rag_runtime/` | Layer 3 | Subsystem modules (Query Analysis, Planner, Fusion, Re-ranking, Citation). |
| `docs/architecture/rag-runtime.md` | Docs | Full architecture specification. |
| `docs/adr/ADR-013-rag-runtime.md` | Docs | This ADR document. |

---

## Related Documents

- Clean Architecture: `docs/architecture/clean-architecture.md`
- Platform Runtime: `docs/architecture/platform-runtime.md`
- Knowledge Base: `docs/architecture/knowledge-base.md`
- Knowledge Graph: `docs/architecture/knowledge-graph.md`
- Memory Layer: `docs/architecture/memory-layer.md`
- Prompt Runtime: `docs/architecture/prompt-runtime.md`
- RAG Spec: `docs/architecture/rag-runtime.md`

---

*Accepted by Lead Architect — 2026-08-04*
