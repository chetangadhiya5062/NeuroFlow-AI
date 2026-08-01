# Backend - Plugin Architecture (`backend/plugins`)

## Purpose
The `plugins` directory powers NeuroFlow AI's **Plugin-First** architecture. It separates domain-independent core platform mechanics from domain-specific intelligence plugins.

## Responsibility
- Provide the official Plugin SDK interfaces that plugin developers extend.
- Discover, validate, register, and manage the lifecycle of domain plugins.
- Provide a clean boundary for domain intelligence modules like Telecom Intelligence.

## Subdirectory Structure
- **`sdk/`**: Base classes, interfaces, and hooks that define plugin contracts.
- **`registry/`**: Dynamic plugin discovery, lifecycle hooks, and plugin metadata management.
- **`telecom/`**: Domain Plugin #1 placeholder directory (Telecom Intelligence).

## What Belongs Here
- Plugin SDK abstractions and interface contracts.
- Plugin loader and registry management code.
- Domain-specific plugin implementations (such as Telecom Intelligence).

## What Does NOT Belong Here
- Platform-wide core domain models.
- General-purpose UI routes or un-isolated core infrastructure.

## Future Roadmap
- Dynamic hot-reloading plugin registry.
- Security sandbox for third-party plugin execution.
- Telecom Intelligence protocol parser plugin implementation.
