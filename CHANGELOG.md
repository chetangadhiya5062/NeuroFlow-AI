<!--
File: CHANGELOG.md
Project: NeuroFlow AI
-->

# Changelog

All notable changes to **NeuroFlow AI** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Repository foundation files (`README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`, `.editorconfig`).
- File identification headers across all repository foundation files.
- Directory scaffolding for canonical runtime alignment (`backend/workflow_engine/`, `backend/agent_runtime/`, `backend/rag_runtime/`, `backend/llm_gateway/`).

---

## [0.1.0-alpha] - 2026-08-05

### Added
- **Phase 1 Architecture Baseline (`docs/architecture/ARCHITECTURE-BASELINE.md`):** Frozen core platform specifications spanning Clean Architecture, Platform Runtime (v2.0.0), Internal Event Bus, AI Memory Layer, Knowledge Base, Knowledge Graph, Workflow Engine (v12.0.0), Agent Runtime (v1.0.0), Tool Runtime, Integration Runtime, Prompt Runtime, and RAG Runtime.
- **Platform Architecture Consistency Review (`docs/architecture/platform_architecture_review.md`):** Completed consistency audit with an 88/100 readiness rating.
- **Implementation Blueprint (`docs/implementation/implementation-blueprint.md`):** Master 9-milestone implementation plan (Milestones 0 to 8), Layer 0–5 package build sequence, constructor injection strategy, testing pyramid, and runtime dependency matrix.
- **Engineering Standards (`docs/development/engineering-standards.md`):** Code quality standards, static typing rules (MyPy), coverage gates (100% Core), structured JSON logging envelope, error hierarchy, and Pull Request checklists.
- **Architecture Decision Record Index (`docs/adr/`):** Accepted ADR-003 through ADR-014 covering runtime execution models, event bus selection, memory store types, state machines, and implementation blueprint.

### Changed
- Resolved directory naming collisions to enforce `workflow_engine`, `agent_runtime`, `rag_runtime`, and `llm_gateway`.
