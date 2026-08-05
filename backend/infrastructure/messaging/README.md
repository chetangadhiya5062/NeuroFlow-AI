<!--
File: backend/infrastructure/messaging/README.md
Project: NeuroFlow AI
-->

# Infrastructure Messaging Package (`backend/infrastructure/messaging/`)

## Purpose
Provides Redis Streams, Kafka, and in-memory event bus and task queue adapters implementing `IEventBusPort` and `ITaskQueuePort`.

## Responsibilities
- Implement `IEventBusPort` for domain event publishing, topic subscription, and consumer group routing.
- Implement `ITaskQueuePort` for asynchronous task enqueueing, worker dispatching, and dead-letter queues.

## Public Interfaces
- `RedisEventBusAdapter`, `KafkaEventBusAdapter`, `RedisTaskQueueAdapter`, `InMemoryEventBusAdapter`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`, `json`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/events/`, `backend/core/exceptions/`).
- Messaging drivers (`redis-py`, `aiokafka`).

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/workflow_engine/`, `backend/agent_runtime/`).

## Related Documents
- `docs/architecture/event-bus.md`
- `docs/adr/ADR-004-event-bus.md`

## Current Status
Scaffolded — Messaging adapters to be implemented in Milestone 2.
