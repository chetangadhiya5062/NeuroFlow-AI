# Layer 0 Core Ports (`backend/core/ports/`)

## Purpose
Contains abstract port interfaces (`IXxxPort`) using Python Abstract Base Classes (`abc.ABC`). All Layer 3 Platform Runtimes depend exclusively on these abstract interfaces. Layer 1 Infrastructure Adapters implement these contracts.

## Rules
- Pure abstract interfaces only.
- Strict MyPy type annotations on all signatures.
- Zero implementation code or technology-specific dependencies.
