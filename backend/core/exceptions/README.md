# Layer 0 Core Platform Exceptions (`backend/core/exceptions/`)

## Purpose
Defines the base exception hierarchy extending `PlatformError`. All custom platform exceptions inherit from classes in this package.

## Hierarchy Summary
- `PlatformError`
  - `ConfigurationError`
  - `AuthorizationError`
  - `ValidationError`
  - `NotFoundError`
  - `ExecutionError`
  - `InfrastructureError`
  - `ResourceExhaustedError`
