<!--
File: backend/core/exceptions/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Exceptions (`backend/core/exceptions/`)

## Purpose
Establishes the platform-wide exception hierarchy extending `PlatformError` to ensure consistent error classification and handling.

## Responsibilities
- Define base platform exception classes for authorization, validation, execution, and infrastructure failures.
- Provide structured exception metadata (error codes, retryable flags, tenant IDs).
- Prevent leak of raw third-party infrastructure exceptions across layer boundaries.

## Public Interfaces
- `PlatformError`, `ConfigurationError`, `AuthorizationError`, `ValidationError`, `NotFoundError`, `ExecutionError`, `InfrastructureError`, `ResourceExhaustedError`

## Allowed Dependencies
- Python standard library (`typing`, `enum`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters or Layer 5 API frameworks.

## Related Documents
- `docs/development/engineering-standards.md`
- `docs/architecture/ARCHITECTURE-BASELINE.md`

## Current Status
Scaffolded — Base exceptions to be implemented in Milestone 1.
