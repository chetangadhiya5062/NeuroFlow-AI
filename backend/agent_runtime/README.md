<!--
File: backend/agent_runtime/README.md
Project: NeuroFlow AI
-->

# Agent Runtime (`backend/agent_runtime/`)

## Purpose
Executes autonomous AI agent reasoning loops, multi-turn decision-making, goal planning, and tool orchestration.

## Responsibilities
- Manage multi-turn agent reasoning state machine and step transitions.
- Coordinate goal decomposition, tool selection, and execution results processing.
- Interact with AI Memory Layer to record episodic interactions.

## Public Interfaces
- `AgentRuntimeEngine`, `IAgentRuntimePort`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Layer 3 Prompt Runtime (`backend/prompt_runtime/`), Tool Runtime (`backend/tool_runtime/`), RAG Runtime (`backend/rag_runtime/`), Memory Layer (`backend/memory_layer/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters directly (must use injected ports).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).
- Heavy AI frameworks (LangChain, LlamaIndex).

## Related Documents
- `docs/architecture/agent-runtime.md`
- `docs/adr/ADR-009-agent-runtime.md`

## Current Status
Scaffolded — To be implemented in Milestone 6.
