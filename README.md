<!--
File: README.md
Project: NeuroFlow AI
-->

# NeuroFlow AI

NeuroFlow AI is a domain-agnostic, production-grade AI Operating Platform designed to orchestrate autonomous AI agents, Retrieval-Augmented Generation (RAG), dynamic workflows, knowledge systems, and domain-specific intelligence plugins.

---

## Architecture Overview

NeuroFlow AI is structured as a Modular Monolith adhering strictly to Clean Architecture and SOLID design principles across six execution layers:

- **Layer 5: Presentation & API Ingress:** FastAPI controllers, OpenAPI schemas, and request/response DTOs.
- **Layer 4: Application Services:** Use-case orchestrators executing application workflows.
- **Layer 3: Platform Runtime:** Core intelligence substrate containing Workflow Engine, Agent Runtime, Tool Runtime, Integration Runtime, Prompt Runtime, RAG Runtime, Knowledge Base, Knowledge Graph, AI Memory Layer, LLM Gateway, and Internal Event Bus.
- **Layer 2: Domain Plugins & Database Models:** Plugin SDK (`NeuroFlowPluginContext`), domain plugins, and ORM persistence entities.
- **Layer 1: Infrastructure Adapters:** Database, vector store, graph, cache, queue, and LLM provider adapters implementing Layer 0 ports.
- **Layer 0: Core Domain Contracts & Ports:** Abstract port interfaces (`IXxxPort`), domain entities, and platform base exceptions.

---

## Repository Structure

```
NeuroFlow-AI/
├── backend/                  # Core Python application engine
│   ├── api/                  # Layer 5: API ingress routes and DTOs
│   ├── services/             # Layer 4: Application use cases
│   ├── agent_runtime/        # Layer 3: Autonomous reasoning engine
│   ├── workflow_engine/      # Layer 3: Execution DAG and state machine
│   ├── rag_runtime/          # Layer 3: Retrieval orchestration
│   ├── prompt_runtime/       # Layer 3: Prompt compilation and context building
│   ├── tool_runtime/         # Layer 3: Tool verification and execution
│   ├── integration_runtime/  # Layer 3: External protocol transport
│   ├── knowledge_base/       # Layer 3: Document management subsystem
│   ├── knowledge_graph/      # Layer 3: Entity-relationship reasoning engine
│   ├── memory_layer/         # Layer 3: Short-term, long-term, and episodic memory
│   ├── llm_gateway/          # Layer 3: Model routing and provider adapters
│   ├── plugins/              # Layer 2: Plugin SDK and domain plugins
│   ├── database/             # Layer 2: Relational database models and migrations
│   ├── infrastructure/       # Layer 1: Concrete storage, queue, and network adapters
│   ├── core/                 # Layer 0: Core contracts, port ABCs, and domain entities
│   └── config/               # Platform settings and dependency injection container
├── docs/                     # Architecture specifications and governance
│   ├── architecture/         # Baseline architecture specifications
│   ├── implementation/       # Implementation blueprints and roadmaps
│   ├── development/          # Coding standards and guidelines
│   └── adr/                  # Architecture Decision Records
├── docker/                   # Container configuration files
├── tests/                    # Unit, integration, contract, and end-to-end tests
├── LICENSE                   # Apache-2.0 License
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Community guidelines
├── SECURITY.md               # Vulnerability reporting and security policy
└── CHANGELOG.md              # Version release history
```

---

## Development Philosophy

- **Interface-First:** All port contracts in `backend/core/ports/` are defined and reviewed prior to adapter or runtime implementation.
- **Build Depth, Not Breadth:** Each milestone delivers a complete, fully tested vertical slice of functionality.
- **Dependency Inversion:** Higher-level layers depend on abstract ports defined in Layer 0. Concrete infrastructure adapters implement ports without exposing technology choices to Layer 3 runtimes.
- **Constructor Injection:** Dependencies are explicitly injected at application startup through `backend/config/container.py`.

---

## Documentation Links

- [**Architecture Baseline**](docs/architecture/ARCHITECTURE-BASELINE.md)
- [**Implementation Blueprint**](docs/implementation/implementation-blueprint.md)
- [**Engineering Standards**](docs/development/engineering-standards.md)
- [**Architecture Decision Records**](docs/adr/)

---

## Roadmap Summary

Platform implementation follows nine sequential milestone gates:

1. **Milestone 0: Foundation:** Governance, repository structure alignment, and tooling setup.
2. **Milestone 1: Core Contracts:** Port interfaces (`backend/core/ports/`), domain entities, and exceptions.
3. **Milestone 2: Infrastructure Layer:** Storage, cache, vector, graph, queue, and LLM provider adapters.
4. **Milestone 3: Storage Subsystems:** Knowledge Base, Knowledge Graph, and AI Memory Layer.
5. **Milestone 4: Retrieval & Prompt:** RAG Runtime, Prompt Runtime, and LLM Gateway.
6. **Milestone 5: Execution Engines:** Tool Runtime, Integration Runtime, and Workflow Engine.
7. **Milestone 6: Intelligence Layer:** Agent Runtime reasoning and execution loop.
8. **Milestone 7: Platform Delivery:** Application services, API controllers, and reference domain plugin.
9. **Milestone 8: Production Readiness:** Load testing, security auditing, and deployment automation.

---

## Contributing

Review [**CONTRIBUTING.md**](CONTRIBUTING.md) for contribution guidelines, branch naming conventions, commit standards, and pull request procedures.

---

## License

NeuroFlow AI is licensed under the [**Apache License, Version 2.0**](LICENSE).
