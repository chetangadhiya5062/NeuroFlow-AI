# Backend - Infrastructure Layer (`backend/infrastructure`)

## Purpose
The `infrastructure` directory houses external technical capabilities and third-party integrations required by the core application (caching, message queues, telemetry, and external web APIs).

## Responsibility
- Implement caching drivers (Redis / Memcached).
- Implement messaging producers/consumers (RabbitMQ / Kafka / NATS).
- Integrate OpenTelemetry metrics, tracing, and logging clients.
- Provide HTTP client wrappers for third-party web services.

## What Belongs Here
- Redis / Caching adapter clients.
- Message queue adapters and event bus drivers.
- Telemetry instrumentation providers.

## What Does NOT Belong Here
- Pure domain models or application use case flows.
- Plugin-specific domain logic (belongs in `backend/plugins/`).

## Future Roadmap
- Distributed caching layer integration.
- OpenTelemetry tracing SDK auto-instrumentation.
