<!--
File: backend/infrastructure/README.md
Project: NeuroFlow AI
-->

# Backend - Infrastructure Layer (`backend/infrastructure/`)

## Purpose
The `infrastructure` directory houses Layer 1 concrete adapters implementing Layer 0 abstract port contracts (`IXxxPort`).

## Infrastructure Packages
- **[`database/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/database/README.md)**: PostgreSQL ORM models, migrations, and repositories.
- **[`cache/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/cache/README.md)**: Redis caching and state persistence adapters.
- **[`vector_store/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/vector_store/README.md)**: Qdrant, pgvector, and memory vector store adapters.
- **[`graph_store/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/graph_store/README.md)**: Neo4j and memory graph database adapters.
- **[`llm/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/llm/README.md)**: OpenAI, Anthropic, and Ollama LLM provider adapters.
- **[`messaging/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/messaging/README.md)**: Redis Streams, Kafka event bus, and task queue adapters.
- **[`storage/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/storage/README.md)**: S3, Azure Blob, and local file storage adapters.
