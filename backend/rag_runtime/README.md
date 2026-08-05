<!--
File: backend/rag_runtime/README.md
Project: NeuroFlow AI
-->

# RAG Runtime (`backend/rag_runtime/`)

## Purpose
Orchestrates hybrid retrieval, vector search, knowledge graph traversal, contextual re-ranking, and citation generation.

## Responsibilities
- Combine vector similarity search with graph path traversal (Graph-RAG).
- Execute contextual re-ranking, score fusion, and result filtering.
- Produce verified citations mapped back to source document chunks.

## Public Interfaces
- `RAGRuntimeEngine`, `IRAGRuntimePort`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Layer 3 Knowledge Base (`backend/knowledge_base/`), Knowledge Graph (`backend/knowledge_graph/`), Memory Layer (`backend/memory_layer/`), LLM Gateway (`backend/llm_gateway/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters directly (must use injected ports).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/rag-runtime.md`
- `docs/adr/ADR-013-rag-runtime.md`

## Current Status
Scaffolded — To be implemented in Milestone 4.
