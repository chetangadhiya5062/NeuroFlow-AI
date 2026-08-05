<!--
File: backend/tool_runtime/README.md
Project: NeuroFlow AI
-->

# Tool Runtime (`backend/tool_runtime/`)

## Purpose
Manages tool registration, verification, argument validation, sandboxed execution, and result transformation.

## Responsibilities
- Validate tool input arguments against Pydantic schemas.
- Execute tools inside unprivileged sandbox execution boundaries.
- Provide integration transport to external APIs via `Integration Runtime`.

## Public Interfaces
- `ToolRuntimeEngine`, `IToolRuntimePort`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Layer 3 Integration Runtime (`backend/integration_runtime/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters directly (must use injected ports).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/tool-runtime.md`
- `docs/adr/ADR-010-tool-runtime.md`

## Current Status
Scaffolded — To be implemented in Milestone 5.
