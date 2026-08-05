<!--
File: backend/integration_runtime/README.md
Project: NeuroFlow AI
-->

# Integration Runtime (`backend/integration_runtime/`)

## Purpose
Handles protocol transformation, external API transport adapters (REST, gRPC, WebSocket), authentication header injection, and network resilience.

## Responsibilities
- Transform domain tool payloads into target HTTP/gRPC wire payloads.
- Handle rate-limit retries, timeout management, and token injection.

## Public Interfaces
- `IntegrationRuntimeEngine`, `IIntegrationRuntimePort`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/exceptions/`).
- Layer 1 Infrastructure Storage/Network Adapters.

## Forbidden Dependencies
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/integration-runtime.md`
- `docs/adr/ADR-011-integration-runtime.md`

## Current Status
Scaffolded — To be implemented in Milestone 5.
