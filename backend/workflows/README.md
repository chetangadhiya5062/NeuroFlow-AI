# Backend - Workflows & DAG Engine (`backend/workflows`)

## Purpose
The `workflows` module handles graph-based pipeline execution, DAG task scheduling, and stateful workflow management in NeuroFlow AI.

## Responsibility
- Define workflow graph node types, edges, and state transitions.
- Execute sequential, parallel, and branching workflow pipelines.
- Manage workflow checkpointing, resume state, and step retry mechanics.

## What Belongs Here
- Workflow execution engine abstractions and task graph solvers.
- Task node contracts (e.g. IngestionNode, PromptNode, AgentNode).
- Workflow state persistence models.

## What Does NOT Belong Here
- Raw HTTP route handlers.
- Specific UI visualization rendering logic.

## Future Roadmap
- Integration with asynchronous message brokers for distributed task execution.
- Dynamic visual workflow graph serialization / deserialization engine.
