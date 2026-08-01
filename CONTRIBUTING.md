# Contributing to NeuroFlow AI

Thank you for your interest in contributing to **NeuroFlow AI**! As an open-source, modular AI platform, we welcome contributions from community members of all skill levels.

---

## 📜 Principles & Standards

1. **Modular Monolith & Clean Architecture**: Maintain clear boundaries between API, core logic, application services, plugins, and infrastructure.
2. **Domain Independence**: Core modules must remain domain-agnostic. Domain specific logic belongs strictly in `backend/plugins/`.
3. **API-First & SOLID Principles**: Design explicit contracts, interfaces, and abstractions before writing implementation code.
4. **Documentation-First**: Ensure all architectural decisions, public APIs, and complex flows are documented.

---

## 🛠️ How to Contribute

### 1. Reporting Issues
- Use GitHub Issue templates to report bugs or suggest enhancements.
- Describe expected vs actual behavior clearly with steps to reproduce.

### 2. Submitting Pull Requests
- Fork the repository and create a descriptive branch name (e.g., `feature/telecom-plugin-sdk` or `fix/rag-indexer-memory`).
- Ensure code complies with Clean Architecture principles.
- Include or update relevant tests and documentation.
- Maintain atomic commits with clean commit messages.

---

## 🔍 Code Review Process
- All pull requests require review and approval from at least one core maintainer.
- Automated CI checks (when active) must pass cleanly.
