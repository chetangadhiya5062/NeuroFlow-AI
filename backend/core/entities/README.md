<!--
File: backend/core/entities/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Entities (`backend/core/entities/`)

## Purpose
Defines domain entities representing primary platform constructs that maintain explicit identity and domain invariants.

## Responsibilities
- Model domain objects with identity (`id`).
- Encapsulate domain rules and state validations.
- Provide pure data structures for platform objects across execution runtimes.

## Public Interfaces
- `AgentDefinition`, `WorkflowDefinition`, `PromptTemplate`, `DocumentChunk`, `KnowledgeGraphEntity`

## Allowed Dependencies
- Python standard library (`typing`, `dataclasses`, `uuid`, `datetime`).
- Pydantic (`pydantic.BaseModel`).
- Core value objects (`backend/core/value_objects/`) and types (`backend/core/types/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters or ORM frameworks (SQLAlchemy, Redis, etc.).
- Layer 3 Platform Runtimes or Layer 4 Services.

## Related Documents
- `docs/architecture/clean-architecture.md`
- `docs/architecture/ARCHITECTURE-BASELINE.md`

## Current Status
Scaffolded — Domain entities to be implemented in Milestone 1.
