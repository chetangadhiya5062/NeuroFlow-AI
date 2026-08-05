<!--
File: backend/infrastructure/README.md
Project: NeuroFlow AI
-->

# Layer 1 Infrastructure Adapters (`backend/infrastructure/`)

## Purpose
Serves as Clean Architecture Layer 1, containing technical adapter implementations of abstract port contracts defined in Layer 0 (`backend/core/ports/`).

## Responsibilities
- Implement concrete data persistence, caching, vector search, graph traversal, messaging, and LLM communication adapters.
- Isolate third-party libraries and drivers behind Layer 0 abstract interfaces.
- Provide `InMemoryXxxAdapter` variants for fast local integration testing.

## Public Interfaces
- Exposed via subpackages: `backend.infrastructure.database`, `backend.infrastructure.cache`, `backend.infrastructure.vector_store`, `backend.infrastructure.graph_store`, `backend.infrastructure.llm`, `backend.infrastructure.messaging`, `backend.infrastructure.storage`.

## Allowed Dependencies
- Python standard library.
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Technology-specific client drivers (SQLAlchemy, Redis, Qdrant, Neo4j, Kafka, OpenAI).

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/*_runtime/`, `backend/workflow_engine/`).
- Layer 4 Services (`backend/services/`).
- Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/clean-architecture.md`
- `docs/implementation/implementation-blueprint.md`

## Current Status
Scaffolded — Adapters to be implemented and contract-tested in Milestone 2.
