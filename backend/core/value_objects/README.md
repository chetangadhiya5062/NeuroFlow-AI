<!--
File: backend/core/value_objects/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Value Objects (`backend/core/value_objects/`)

## Purpose
Defines immutable, identity-less value objects that encapsulate domain measurements, identifiers, status states, and attributes.

## Responsibilities
- Provide immutable value wrappers for platform identifiers and domain attributes.
- Ensure structural equality and validation upon instantiation.

## Public Interfaces
- `TenantId`, `WorkflowExecutionId`, `EmbeddingVector`, `TokenBudget`

## Allowed Dependencies
- Python standard library (`typing`, `dataclasses`, `uuid`, `datetime`).
- Pydantic (`pydantic.BaseModel`).
- Core types (`backend/core/types/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters or Layer 3 Platform Runtimes.

## Related Documents
- `docs/architecture/clean-architecture.md`

## Current Status
Scaffolded — Value objects to be implemented in Milestone 1.
