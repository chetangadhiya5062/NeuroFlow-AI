<!--
File: backend/infrastructure/database/README.md
Project: NeuroFlow AI
-->

# Infrastructure Database Package (`backend/infrastructure/database/`)

## Purpose
Provides PostgreSQL database persistence adapters, ORM entity mappings, migration scripts, and repository implementations.

## Responsibilities
- Implement relational database persistence ports defined in `backend/core/ports/`.
- Manage SQLAlchemy/asyncpg ORM models, session factories, and connection pooling.
- Manage database schema migrations (Alembic).

## Public Interfaces
- `PostgresWorkflowStateRepository`, `PostgresTenantRepository`

## Allowed Dependencies
- Python standard library (`typing`, `contextlib`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- SQLAlchemy, asyncpg, Alembic.

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/*_runtime/`, `backend/workflow_engine/`).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/clean-architecture.md`
- `docs/implementation/implementation-blueprint.md`

## Current Status
Scaffolded — Relational database adapters to be implemented in Milestone 2.
