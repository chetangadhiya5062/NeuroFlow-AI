# Layer 0 Core Domain Entities (`backend/core/entities/`)

## Purpose
Defines domain entities representing core platform constructs (e.g., `AgentDefinition`, `WorkflowDefinition`, `PromptTemplate`, `DocumentChunk`, `KnowledgeGraphEntity`).

## Rules
- Pure dataclasses or Pydantic models with identity.
- Encapsulates domain invariants and business rules.
- Free of infrastructure logic, ORM mappings, or network protocols.
