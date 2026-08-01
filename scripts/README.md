# Automation & Developer Scripts (`scripts/`)

## Purpose
The `scripts` directory houses shell, Python, and utility automation scripts used for project bootstrapping, database migration triggers, code generation, and developer onboarding.

## Responsibility
- Provide automated setup scripts for local development environments.
- Provide helper scripts for linting, database seeding, and code validation.
- Automate repetitive developer tasks across backend and frontend environments.

## What Belongs Here
- Shell (`.sh` / `.ps1`) and Python automation scripts.
- Environment setup and validation utilities.

## What Does NOT Belong Here
- Application runtime services or core domain logic.
- CI/CD workflow definitions (belongs in `.github/workflows/`).

## Future Roadmap
- Local dev environment bootstrap script (`scripts/setup_dev.py`).
- Plugin scaffolding generator script (`scripts/create_plugin.py`).
