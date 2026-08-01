# Backend - API Layer (`backend/api`)

## Purpose
The `api` module provides the external interface layer for NeuroFlow AI, handling incoming HTTP/gRPC requests, routing, serializing responses, and enforcing API security.

## Responsibility
- Expose RESTful and WebSocket API endpoints.
- Parse, validate, and sanitize request payloads.
- Handle request authentication, authorization, and rate limiting.
- Format application service responses into versioned API outputs.

## What Belongs Here
- Route definitions and HTTP controllers.
- Request and response Data Transfer Objects (DTOs) / Pydantic schemas.
- API versioning logic (e.g., `/v1/`, `/v2/`).
- API-level middleware (CORS, auth context extraction, request logging).

## What Does NOT Belong Here
- Core business logic or domain rules.
- Database access or direct SQL queries.
- LLM prompt building or direct provider invocations.

## Future Roadmap
- OpenAPI / Swagger schema generation.
- Rate limiting and API key management middleware.
- Event-driven WebSocket streaming endpoints for real-time AI agent responses.
