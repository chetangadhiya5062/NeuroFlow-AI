<!--
File: backend/core/types/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Types (`backend/core/types/`)

## Purpose
Contains shared domain enumerations, type aliases, and primitive declarations used across all Clean Architecture layers.

## Responsibilities
- Define standard platform status enumerations (`TaskStatus`, `AgentExecutionState`, `MemoryType`).
- Provide type aliases for system primitives and IDs.

## Public Interfaces
- `TaskStatus`, `AgentExecutionState`, `MemoryType`, `LogLevel`, `VectorDistanceMetric`

## Allowed Dependencies
- Python standard library (`typing`, `enum`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters or Layer 3 Platform Runtimes.

## Related Documents
- `docs/architecture/clean-architecture.md`

## Current Status
Scaffolded — Core types to be declared in Milestone 1.
