<!--
File: backend/infrastructure/llm/README.md
Project: NeuroFlow AI
-->

# Infrastructure LLM Package (`backend/infrastructure/llm/`)

## Purpose
Provides OpenAI, Anthropic, Ollama, and mock LLM provider adapters implementing `ILLMProviderPort`.

## Responsibilities
- Implement `ILLMProviderPort` for text completion, chat generation, structured output, and embeddings.
- Translate domain requests into provider-specific API wire formats and handle network retries.

## Public Interfaces
- `OpenAILLMAdapter`, `AnthropicLLMAdapter`, `OllamaLLMAdapter`, `MockLLMAdapter`

## Allowed Dependencies
- Python standard library (`typing`, `asyncio`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Provider HTTP/REST SDKs (`httpx`, `openai`, `anthropic`).

## Forbidden Dependencies
- Layer 3 Platform Runtimes (`backend/llm_gateway/`, `backend/prompt_runtime/`, `backend/agent_runtime/`).

## Related Documents
- `docs/architecture/prompt-runtime.md`
- `docs/architecture/platform-runtime.md`

## Current Status
Scaffolded — LLM provider adapters to be implemented in Milestone 2.
