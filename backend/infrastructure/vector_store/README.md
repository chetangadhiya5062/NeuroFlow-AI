<!--
File: backend/infrastructure/vector_store/README.md
Project: NeuroFlow AI
-->

# Infrastructure Vector Store Package (`backend/infrastructure/vector_store/`)

## Purpose
Provides Qdrant, pgvector, and in-memory vector database adapters implementing `IVectorStorePort`.

## Responsibilities
- Implement `IVectorStorePort` for vector embedding persistence, payload filtering, and similarity search.
- Manage vector collection creation, indexing, distance metrics, and batch insertion.

## Public Interfaces
- `QdrantVectorStoreAdapter`, `PgVectorStoreAdapter`, `InMemoryVectorStoreAdapter`

## Allowed Dependencies
- Python standard library (`typing`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Vector store SDKs (`qdrant-client`).

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/knowledge_base/`, `backend/rag_runtime/`).

## Related Documents
- `docs/architecture/knowledge-base.md`
- `docs/adr/ADR-006-knowledge-base.md`

## Current Status
Scaffolded — Vector store adapters to be implemented in Milestone 2.
