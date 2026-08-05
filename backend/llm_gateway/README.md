<!--
File: backend/llm_gateway/README.md
Project: NeuroFlow AI
-->

# LLM Gateway (`backend/llm_gateway/`)

## Purpose
Provides unified model routing, provider fallback, rate limiting, token budget management, and response normalization across heterogeneous LLM providers.

## Responsibilities
- Route LLM requests to target providers based on model tier and availability.
- Handle automatic provider fallbacks and circuit breaker state.
- Normalize heterogeneous provider responses into standard domain schemas.

## Public Interfaces
- `LLMGatewayService`, `ILLMGatewayPort`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Layer 1 LLM Infrastructure Adapters (`backend/infrastructure/llm/`).

## Forbidden Dependencies
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/platform-runtime.md`

## Current Status
Scaffolded — To be implemented in Milestone 4.
