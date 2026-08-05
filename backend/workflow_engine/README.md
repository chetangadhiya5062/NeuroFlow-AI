<!--
File: backend/workflow_engine/README.md
Project: NeuroFlow AI
-->

# Workflow Engine (`backend/workflow_engine/`)

## Purpose
Orchestrates DAG-based execution workflows, state machines, task queues, checkpointing, and Saga compensation rollbacks.

## Responsibilities
- Parse and validate workflow DSL definitions and task dependencies.
- Execute task DAGs with dynamic conditional branching and parallel dispatching.
- Manage execution checkpoints and handle compensation rollbacks upon task failure.

## Public Interfaces
- `WorkflowEngineService`, `IWorkflowEnginePort`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters directly (must use injected ports).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/workflow-engine.md`
- `docs/adr/ADR-008-workflow-engine.md`

## Current Status
Scaffolded — To be implemented in Milestone 5.
