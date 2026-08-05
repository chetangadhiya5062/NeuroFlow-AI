<!--
File: backend/core/ports/README.md
Project: NeuroFlow AI
-->

# Layer 0 Core Ports (`backend/core/ports/`)

## Purpose
Defines pure abstract port interfaces (`IXxxPort`) using Python Abstract Base Classes (`abc.ABC`) to establish Clean Architecture boundary contracts across all subsystems.

## Responsibilities
- Define abstract method signatures, input parameters, and return types for system interfaces.
- Specify strict static type annotations for all interface parameters.
- Provide contract definitions for storage, messaging, LLMs, and platform runtimes.

## Public Interfaces
- `IVectorStorePort`, `IGraphStorePort`, `IMemoryStorePort`, `IStoragePort`, `ICheckpointStorePort`
- `IEventBusPort`, `ITaskQueuePort`
- `ILLMProviderPort`, `IToolExecutorPort`, `IWorkflowEnginePort`, `IAgentRuntimePort`

## Allowed Dependencies
- Python standard library (`abc`, `typing`, `enum`, `dataclasses`, `uuid`, `datetime`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters (`backend/infrastructure/`).
- Layer 3 Platform Runtimes (`backend/*_runtime/`, `backend/workflow_engine/`, etc.).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).
- Third-party database, vector, or LLM provider SDKs (e.g., Qdrant, Neo4j, Redis, OpenAI).

## Related Documents
- `docs/architecture/clean-architecture.md`
- `docs/architecture/ARCHITECTURE-BASELINE.md`

## Current Status
Scaffolded — Interface signatures to be declared in Milestone 1.
