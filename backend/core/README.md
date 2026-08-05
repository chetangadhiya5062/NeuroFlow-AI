<!--
File: backend/core/README.md
Project: NeuroFlow AI
-->

# Backend - Core Domain Layer (`backend/core/`)

## Purpose
The `core` directory forms Clean Architecture Layer 0 in NeuroFlow AI. It contains pure domain entities, value objects, abstract port contracts, exceptions, events, and types.

## Core Packages
- **[`ports/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/ports/README.md)**: Abstract port interfaces (`IXxxPort`) defining system boundaries.
- **[`entities/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/entities/README.md)**: Domain entities with identity and business invariants.
- **[`exceptions/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/exceptions/README.md)**: Base platform exception hierarchy extending `PlatformError`.
- **[`value_objects/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/value_objects/README.md)**: Immutable, identity-less domain values.
- **[`events/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/events/README.md)**: Domain event types for event-driven orchestration.
- **[`types/`](file:///d:/Ghanu_Study/Varnagi_Learning/Projects/GitHub/Internship-Project/NeuroFlow-AI/backend/core/types/README.md)**: Shared domain enums, type aliases, and primitive declarations.
