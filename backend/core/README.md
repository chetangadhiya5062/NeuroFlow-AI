# Backend - Core Domain Layer (`backend/core`)

## Purpose
The `core` module forms the heart of Clean Architecture in NeuroFlow AI. It contains domain entities, value objects, domain contracts, and core domain exceptions.

## Responsibility
- Define pure domain models independent of frameworks, databases, or UI layers.
- Specify interface contracts (Abstract Base Classes / Protocols) required by upper layers.
- Maintain core domain invariants and domain events.

## What Belongs Here
- Domain Entities and Value Objects.
- Abstract repository contracts & interface declarations.
- Domain-level exceptions (e.g., `PluginNotFoundException`, `WorkflowExecutionError`).
- Core constants and domain enumerations.

## What Does NOT Belong Here
- Framework-specific imports (FastAPI, SQLAlchemy, Pydantic DB decorators).
- HTTP routing code or database connection code.
- Specific AI provider SDK calls.

## Future Roadmap
- Domain event dispatcher interface.
- Core telemetry and audit event definitions.
