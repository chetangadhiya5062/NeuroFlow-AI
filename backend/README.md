<!--
File: backend/README.md
Project: NeuroFlow AI
-->

# NeuroFlow AI — Backend Application Engine

## Purpose
The `backend` directory contains the server-side application engine of **NeuroFlow AI**. It is structured as a **Modular Monolith** adhering strictly to **Clean Architecture** and **SOLID** design principles across Layers 0 to 5.

## Architectural Structure

- **[`core/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/README.md)**: Layer 0 Core contracts (`ports/`), domain models (`entities/`, `value_objects/`), exceptions (`exceptions/`), events (`events/`), and primitive definitions (`types/`).
- **[`infrastructure/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/infrastructure/README.md)**: Layer 1 Infrastructure adapters (`database/`, `cache/`, `vector_store/`, `graph_store/`, `llm/`, `messaging/`, `storage/`).
- **Layer 3 Platform Runtimes (Intelligence Substrate):**
  - **[`agent_runtime/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/agent_runtime/README.md)**: Autonomous agent reasoning loops and multi-turn decision execution.
  - **[`workflow_engine/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/workflow_engine/README.md)**: DAG-based execution workflow engine and state machine.
  - **[`rag_runtime/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/rag_runtime/README.md)**: Retrieval orchestration, hybrid fusion, and context re-ranking.
  - **[`prompt_runtime/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/prompt_runtime/README.md)**: Prompt template compilation and multi-block context builder.
  - **[`llm_gateway/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/llm_gateway/README.md)**: Multi-provider model routing, fallback management, and rate-limiting.
  - **[`tool_runtime/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/tool_runtime/README.md)**: Tool discovery, verification, and sandboxed execution.
  - **[`integration_runtime/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/integration_runtime/README.md)**: External protocol adapters (REST, gRPC, WebSocket).
  - **[`knowledge_base/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/knowledge_base/README.md)**: Document management, chunking, and embedding pipelines.
  - **[`knowledge_graph/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/knowledge_graph/README.md)**: Entity-relationship reasoning and path traversal engine.
  - **[`memory_layer/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/memory_layer/README.md)**: Short-term, long-term, episodic, and entity memory subsystems.
- **[`services/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/services/README.md)**: Layer 4 Application use-case orchestrators.
- **[`api/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/api/README.md)**: Layer 5 FastAPI routes, controllers, and schema DTOs.
- **[`config/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/config/README.md)**: Environment settings, feature flags, and Dependency Injection container.

## What Does NOT Belong Here
- Web UI frontend code (lives in `frontend/`).
- Domain plugins or Plugin SDK (lives in `plugins/` at repository root).
- Automated test suites (lives in `tests/` at repository root).
