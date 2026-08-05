<!--
File: backend/prompt_runtime/README.md
Project: NeuroFlow AI
-->

# Prompt Runtime (`backend/prompt_runtime/`)

## Purpose
Manages prompt template compilation, versioning, context assembly, multi-block construction, and safety policy injection.

## Responsibilities
- Compile parameterized Jinja2 prompt templates with dynamic variables.
- Assemble multi-block context payloads (system instructions, retrieved context, memory history, user prompt).
- Enforce token budgets and apply safety guardrail filters.

## Public Interfaces
- `PromptRuntimeEngine`, `IPromptRuntimePort`

## Allowed Dependencies
- Python standard library (`typing`).
- Layer 0 Core contracts (`backend/core/ports/`, `backend/core/entities/`, `backend/core/exceptions/`).
- Layer 3 LLM Gateway (`backend/llm_gateway/`), Memory Layer (`backend/memory_layer/`), RAG Runtime (`backend/rag_runtime/`).

## Forbidden Dependencies
- Layer 1 Infrastructure Adapters directly (must use injected ports).
- Layer 4 Services (`backend/services/`) or Layer 5 API Ingress (`backend/api/`).

## Related Documents
- `docs/architecture/prompt-runtime.md`
- `docs/adr/ADR-012-prompt-runtime.md`

## Current Status
Scaffolded — To be implemented in Milestone 4.
