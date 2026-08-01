# NeuroFlow AI - Technical Documentation (`docs/`)

## Purpose
The `docs` directory maintains system specifications, architecture documents, API schemas, Architecture Decision Records (ADRs), visual diagrams, and engineering decision logs for **NeuroFlow AI**.

## Responsibility
- Document high-level system architecture and Clean Architecture principles.
- Maintain a record of major architectural decisions via ADRs.
- Store OpenAPI specifications and API contract documentation.
- Maintain visual flowcharts, sequence diagrams, and engineering choice records.

## Subdirectory Structure
- **`architecture/`**: High-level framework design, domain independence specs, and modular monolith architecture docs.
- **`adr/`**: Architecture Decision Records (ADRs) tracking significant system decisions.
- **`api/`**: OpenAPI / AsyncAPI specifications, endpoint schemas, and versioning rules.
- **`diagrams/`**: Visual diagrams (Mermaid, C4 architecture model, sequence diagrams).
- **`decisions/`**: Log of lightweight engineering decisions and trade-off evaluations.

## What Belongs Here
- Markdown documentation, Mermaid diagram source files, and OpenAPI JSON/YAML schemas.
- Technical specs for domain plugin interfaces and RAG pipelines.

## What Does NOT Belong Here
- Executable application code or inline code comments.
- Raw temporary scratch notes or internal credentials.

## Future Roadmap
- Publish automated documentation builder to render static technical docs.
- Add initial ADRs for Plugin Architecture and Vector DB integration strategies.
