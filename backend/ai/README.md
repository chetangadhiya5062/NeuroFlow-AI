# Backend - AI Foundation Layer (`backend/ai`)

## Purpose
The `ai` module houses provider abstractions, prompt templates, model wrappers, and tool definitions required for AI inference across the platform.

## Responsibility
- Decouple application logic from specific LLM providers (e.g. OpenAI, Anthropic, Gemini, local models).
- Manage structured prompt templates and versioning.
- Expose model definition wrappers and token management tools.
- Provide executable tool interfaces usable by AI agents.

## Subdirectory Structure
- **`providers/`**: LLM & multimodal API vendor adapters.
- **`prompts/`**: Prompt templates, dynamic prompt generators, and versioned system prompts.
- **`models/`**: Unified model input/output abstraction schemas and tokenizers.
- **`tools/`**: Tool definitions and execution wrappers for model tool-calling.

## What Belongs Here
- Provider client adapters implementing standardized AI interfaces.
- Structured prompt management system and schemas.
- Custom LLM tool schemas and function invocation wrappers.

## What Does NOT Belong Here
- RAG document ingestion pipelines (belongs in `backend/rag/`).
- Autonomous agent state machines (belongs in `backend/agents/`).
- Application HTTP handlers.

## Future Roadmap
- Multi-provider fallback and load-balancing router.
- Token consumption tracking and cost estimation metrics.
- Local model runtime connector (Ollama / vLLM adapter).
