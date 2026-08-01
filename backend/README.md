# NeuroFlow AI - Backend Core Engine

## Purpose
The `backend` directory contains the server-side application engine of **NeuroFlow AI**. It is structured as a **Modular Monolith** adhering strictly to **Clean Architecture** and **SOLID** design principles.

## Responsibility
- Execute domain-agnostic AI orchestrations, agent workflows, and RAG pipelines.
- Expose clear, versioned API contracts to the frontend and external API consumers.
- Host the core domain model, application service layer, database persistence abstractions, and plugin SDK/registry.

## What Belongs Here
- **[`api/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/api/README.md)**: HTTP API routes, controllers, request/response models, middleware.
- **[`core/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/README.md)**: Core domain entities, contracts, interfaces, and domain exceptions.
- **[`config/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/config/README.md)**: Environment settings, feature flags, dependency injection composition.
- **[`services/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/services/README.md)**: Application use-case orchestrators and domain services.
- **[`plugins/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/plugins/README.md)**: Plugin architecture (SDK, registry, domain plugins like Telecom).
- **[`ai/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/ai/README.md)**: LLM abstractions, provider connectors, prompt management, agent tools.
- **[`rag/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/rag/README.md)**: Document ingestion, embedding generation, vector retrieval, and indexing.
- **[`agents/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/agents/README.md)**: Autonomous agent orchestrators, planners, memory managers.
- **[`workflows/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/workflows/README.md)**: DAG workflow engine and pipeline execution graphs.
- **[`database/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/database/README.md)**: Database migrations, repositories, ORM models, and seeders.
- **[`infrastructure/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/README.md)**: Caching, messaging queues, telemetry, and external API clients.
- **[`tests/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/tests/README.md)**: Backend test suites (unit, integration, e2e, fixtures).

## What Does NOT Belong Here
- Web UI components or frontend presentation code.
- Hardcoded domain business logic outside of domain plugins.
- Deployment scripts or raw infra provisioners.

## Future Roadmap
- Implement FastAPI/ASGI application initialization.
- Implement Plugin discovery loader and dynamic hook invocation system.
- Integrate multi-tenant vector database adapters.
