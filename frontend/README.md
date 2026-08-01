# NeuroFlow AI - Frontend Web Application (`frontend/`)

## Purpose
The `frontend` directory contains the web user interface for **NeuroFlow AI**, architected around **Next.js App Router** conventions.

## Responsibility
- Provide an intuitive, modern user interface for managing AI workflows, domain plugins, RAG knowledge bases, and AI agent execution.
- Maintain a clean presentation layer isolated from backend execution engines.
- Handle user authentication, interactive visualizations, and real-time event streaming.

## Subdirectory Structure
- **`app/`**: Next.js App Router layout boundaries, pages, route handlers, and server components.
- **`components/`**: Reusable design system UI components (buttons, modals, cards, inputs).
- **`features/`**: Domain and plugin feature modules (e.g. Telecom analytics views, RAG document managers).
- **`lib/`**: Shared client utility functions, API client configurations, and constants.
- **`hooks/`**: Custom React hooks for state management, data fetching, and event subscriptions.
- **`styles/`**: Global CSS, theme definitions, and design tokens.
- **`types/`**: Shared TypeScript interfaces, type aliases, and API contract types.
- **`public/`**: Public static assets, icons, fonts, and images.

## What Belongs Here
- Next.js web application code, React components, CSS styles, and client state hooks.
- TypeScript interfaces matching backend API responses.

## What Does NOT Belong Here
- Backend domain entities, SQL queries, or direct database connections.
- Raw Python code or backend plugin execution handlers.

## Future Roadmap
- Initialize Next.js project dependencies and Tailwind CSS / custom design tokens.
- Implement workflow graph visual editor component.
- Integrate real-time WebSocket client for streaming agent responses.
