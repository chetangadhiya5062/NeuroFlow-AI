<!--
File: backend/core/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Domain Layer (`backend/core/`)

## Purpose
Serves as Clean Architecture Layer 0, housing pure domain contracts, entities, exceptions, value objects, domain events, and primitive types.

## Responsibilities
- Provide abstract interface contracts (`ports/`) that define system boundaries.
- Define identity-bearing domain entities (`entities/`) and immutable values (`value_objects/`).
- Establish the platform base exception hierarchy (`exceptions/`).
- Model event payload structures (`events/`) and core enumerations (`types/`).

## Public Interfaces
- Exposed via subpackages: `backend.core.ports`, `backend.core.entities`, `backend.core.exceptions`, `backend.core.value_objects`, `backend.core.events`, `backend.core.types`.

## Allowed Dependencies
- Python standard library (`abc`, `typing`, `enum`, `dataclasses`, `uuid`, `datetime`).
- Pydantic (`pydantic.BaseModel`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters (`backend/infrastructure/`).
- Layer 3 Platform Runtimes (`backend/*_runtime/`, `backend/workflow_engine/`).
- Layer 4 Application Services (`backend/services/`).
- Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/clean-architecture.md`
- `docs/architecture/ARCHITECTURE-BASELINE.md`

## Current Status
Scaffolded — Interface contracts and domain entities to be implemented in Milestone 1.
