# Backend - Application Services Layer (`backend/services`)

## Purpose
The `services` layer orchestrates use cases in NeuroFlow AI by translating user intents into operations across core domain entities, AI agents, RAG engines, and data repositories.

## Responsibility
- Implement application use cases and business workflow orchestrations.
- Enforce cross-cutting transaction boundaries, validation, and domain service rules.
- Coordinate interaction between backend modules (e.g., triggering RAG ingestion before AI agent processing).

## What Belongs Here
- Application service classes (e.g., `WorkflowExecutionService`, `PluginManagementService`).
- Use-case execution handlers and transaction orchestrators.
- Event handlers processing internal domain events.

## What Does NOT Belong Here
- HTTP protocol request/response parsing (belongs in `api/`).
- Direct SQL queries or database ORM mapping (belongs in `database/`).
- Vendor-specific AI client implementations (belongs in `ai/providers/`).

## Future Roadmap
- Asynchronous task dispatch integration via background workers.
- Granular service instrumentation for tracing and metrics collection.
