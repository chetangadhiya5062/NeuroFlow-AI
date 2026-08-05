<!--
File: backend/infrastructure/graph_store/README.md
Project: NeuroFlow AI
-->

# Infrastructure Graph Store Package (`backend/infrastructure/graph_store/`)

## Purpose
Provides Neo4j and in-memory graph database adapters implementing `IGraphStorePort`.

## Responsibilities
- Implement `IGraphStorePort` for entity node, relationship, and graph trajectory persistence.
- Manage Cypher query execution, path traversal algorithms, and graph schema constraints.

## Public Interfaces
- `Neo4jGraphStoreAdapter`, `InMemoryGraphStoreAdapter`

## Allowed Dependencies
- Python standard library (`typing`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Graph database SDKs (`neo4j`).

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/knowledge_graph/`).

## Related Documents
- `docs/architecture/knowledge-graph.md`
- `docs/adr/ADR-007-knowledge-graph.md`

## Current Status
Scaffolded — Graph store adapters to be implemented in Milestone 2.
