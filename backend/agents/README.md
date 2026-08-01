# Backend - Autonomous Agents Framework (`backend/agents`)

## Purpose
The `agents` directory implements the autonomous AI agent execution engine, managing reasoning loops, multi-step planning, tool usage, and memory persistence.

## Responsibility
- Execute agent reasoning and plan generation loops (e.g. ReAct / Plan-and-Solve).
- Maintain short-term working memory and long-term agent memory stores.
- Bind domain and platform tools to agent execution contexts.
- Coordinate multi-agent communication and task delegation.

## Subdirectory Structure
- **`orchestrator/`**: Main agent execution loops, multi-agent orchestrator, and runtime supervision.
- **`memory/`**: Conversation history, working memory buffers, and long-term vector memory adapters.
- **`tools/`**: Agent-specific tool bindings and sandboxed tool execution handlers.
- **`planner/`**: Task decomposition, goal planning, and reflection/critique engines.

## What Belongs Here
- Agent execution state machines and orchestrator loops.
- Planning algorithms and goal-satisfaction verifiers.
- Agent memory state managers.

## What Does NOT Belong Here
- Low-level LLM API HTTP calls (belongs in `backend/ai/`).
- Direct database schema definitions (belongs in `backend/database/`).

## Future Roadmap
- Multi-agent collaboration protocols (hierarchical and consensus-based).
- Human-in-the-loop approval step integration for agent tool calls.
