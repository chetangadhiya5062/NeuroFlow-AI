# Backend - Database Layer (`backend/database`)

## Purpose
The `database` directory encapsulates data persistence, ORM data models, repository implementations, schema migrations, and database seed scripts.

## Responsibility
- Implement data access logic following the Repository Pattern.
- Define relational/document database schemas and ORM mappings.
- Manage database schema migrations and versioning.
- Provide seed data scripts for local development and testing environments.

## Subdirectory Structure
- **`migrations/`**: Schema migration scripts (e.g. Alembic / SQL migrations).
- **`repositories/`**: Concrete repository pattern persistence classes implementing core interface contracts.
- **`models/`**: ORM entity definitions and database tables schemas.
- **`seeds/`**: Initial database seed data scripts and fixtures.

## What Belongs Here
- ORM model definitions (SQLAlchemy / SQLModel / Prisma schemas).
- Repository implementations and data access helpers.
- Migration scripts and seeders.

## What Does NOT Belong Here
- Pure domain entities (belongs in `backend/core/`).
- HTTP API controller handlers (belongs in `backend/api/`).

## Future Roadmap
- Alembic migration environment configuration.
- Read/write database replica splitting support.
