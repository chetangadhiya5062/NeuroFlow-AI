<!--
File: backend/core/events/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Events (`backend/core/events/`)

## Purpose
Defines domain event payload schemas published across the Internal Event Bus during platform operation.

## Responsibilities
- Model event data structures published by runtimes and application services.
- Provide standard event envelopes (event ID, timestamp, trace context, tenant ID).

## Public Interfaces
- `TaskCompletedEvent`, `WorkflowStartedEvent`, `AgentReasoningStepEvent`, `DocumentIngestedEvent`

## Allowed Dependencies
- Python standard library (`typing`, `uuid`, `datetime`).
- Pydantic (`pydantic.BaseModel`).
- Core value objects (`backend/core/value_objects/`) and types (`backend/core/types/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters (Kafka, Redis Streams).
- Layer 3 Platform Runtimes or Layer 5 API Ingress.

## Related Documents
- `docs/architecture/event-bus.md`
- `docs/adr/ADR-004-event-bus.md`

## Current Status
Scaffolded — Domain events to be defined in Milestone 1.
