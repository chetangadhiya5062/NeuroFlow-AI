<!--
File: backend/infrastructure/cache/README.md
Project: NeuroFlow AI
-->

# Infrastructure Cache Package (`backend/infrastructure/cache/`)

## Purpose
Provides Redis and in-memory caching adapters implementing core caching and memory store ports.

## Responsibilities
- Implement `ICachePort` and `IMemoryStorePort` contracts.
- Manage key-value caching, key expiration, serialization, and connection pooling.

## Public Interfaces
- `RedisCacheAdapter`, `InMemoryCacheAdapter`

## Allowed Dependencies
- Python standard library (`typing`, `json`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/exceptions/`).
- Redis client (`redis-py`).

## Forbidden Dependencies
- Layer 3 Platform Runtimes or Layer 4 Services.

## Related Documents
- `docs/architecture/memory-layer.md`
- `docs/adr/ADR-005-memory-layer.md`

## Current Status
Scaffolded — Cache adapters to be implemented in Milestone 2.
