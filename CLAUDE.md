# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mail2Audio is a full-stack application that converts email newsletters into audio clips using Amazon Polly TTS. Users can upload .eml files or link their Gmail account to generate audio from their subscribed newsletters.

**Stack:**
- Backend: FastAPI (Python) with SQLAlchemy ORM
- Frontend: React 19 + TypeScript + Vite
- Database: SQLite (development)
- Architecture: Repository pattern with service layer

## Monorepo Structure

```
mail2audio/
├── packages/
│   ├── api/                    ← Python FastAPI backend
│   │   ├── app/                ← Application code
│   │   ├── tests/              ← Test suite
│   │   └── pyproject.toml      ← Python project config
│   └── web/                    ← React frontend
│       ├── src/
│       ├── package.json
│       └── vite.config.ts
├── docs/                       ← Shared documentation
├── infrastructure/             ← Shared infra
├── package.json                ← Root: npm workspaces + dev orchestration
└── CLAUDE.md
```

## Development Commands

### Running the application

```bash
# Start both API and frontend concurrently (recommended)
npm run dev

# Or run separately:
# Backend only (FastAPI dev server on :8000)
cd packages/api && fastapi dev app/main.py

# Frontend only (Vite dev server on :5173, proxies to :8000)
cd packages/web && npm run dev
```

### Testing

```bash
# Run all tests with coverage (from packages/api/)
cd packages/api && pytest

# Run specific test file
cd packages/api && pytest tests/test_services/test_email_service.py

# Run with verbose output
cd packages/api && pytest -v

# Run specific test by name
cd packages/api && pytest -k "test_parse_eml_file"
```

### Frontend

```bash
cd packages/web

# Build for production
npm run build

# Lint
npm run lint

# Preview production build
npm run preview
```

## Architecture

### Backend Structure (packages/api/app/)

The backend follows a **layered architecture** with clear separation of concerns:

```
routers/      → API endpoints (HTTP layer)
    ↓
services/     → Business logic orchestration
    ↓
repositories/ → Data access layer (ORM queries)
    ↓
models/       → SQLAlchemy ORM models
```

**Key patterns:**
- `models/base.py` exports the SQLAlchemy `Base` class used by all ORM models
- `db/database.py` provides the `engine`, `SessionLocal`, and `get_db()` dependency
- Database tables are auto-created on app startup via `Base.metadata.create_all()` in `main.py`
- Services use FastAPI's `Depends()` for dependency injection of repositories
- Pydantic schemas in `schemas/` handle request/response validation and ORM-to-dict conversion using `.model_validate()`

**Email processing flow:**
1. Router receives .eml file upload → `routers/emails.py`
2. EmailService orchestrates parsing and persistence → `services/email_service.py`
3. EmailParser extracts metadata and HTML-to-text conversion → `services/email_parser.py`
4. EmailRepository handles database operations → `repositories/email.py`
5. Returns Pydantic schema via `.model_validate()` for API response

**Important details:**
- HTML text extraction uses a custom `HTMLTextExtractor(HTMLParser)` class in `email_parser.py` that skips `<script>` and `<style>` tags
- Email validation requires both `subject` and `sender` fields in `EmailService.process_file()`
- The SQLite database file is `mail2audio.db` in `packages/api/`

### Frontend Structure (packages/web/src/)

```
pages/          → Route components (Landing, Dashboard, EmailDetail)
components/     → Reusable UI components
services/       → API client (emailApi.ts communicates with FastAPI)
hooks/          → Custom React hooks (useAuth, useEmailUpload)
types/          → TypeScript type definitions
```

**Key integration points:**
- Vite proxies `/api` and `/auth` requests to `http://localhost:8000` (see `packages/web/vite.config.ts`)
- `emailApi.ts` handles all API communication with proper error handling
- React Router v7 manages client-side routing

## Database

- **Type:** SQLite (file: `packages/api/mail2audio.db`)
- **ORM:** SQLAlchemy with declarative base
- **Schema:** Auto-created on startup, no migrations currently configured
- **Models:** `Email` (email_model.py), `User` (user_model.py - in progress)

To reset the database, delete `packages/api/mail2audio.db` and restart the server.

## Authentication (In Progress)

Gmail OAuth integration is partially implemented:
- `packages/api/app/auth/gmail_oauth_client.py` contains OAuth client
- `packages/api/app/routers/auth.py` exists but is commented out in `main.py`
- Frontend has `useAuth` hook and Google sign-in buttons

## Testing Strategy

- Tests mirror the `app/` directory structure in `packages/api/tests/`
- `packages/api/tests/conftest.py` provides shared fixtures: `test_app`, `client`, `sample_email_html`
- Use `TestClient` from FastAPI for router integration tests
- Repository tests should mock database interactions
- Service tests should test business logic with mocked repositories

## Common Gotchas

1. **Email parsing**: Only .eml files are supported. The parser expects HTML content and converts to plain text
2. **Database session**: Always use `get_db()` dependency for database sessions in routes
3. **Schema conversion**: Use `.model_validate(orm_instance)` to convert SQLAlchemy models to Pydantic schemas
4. **Proxy configuration**: Frontend API calls work via Vite proxy in dev; production needs different setup
5. **Date parsing**: Email dates use `parsedate_to_datetime()` and can return None if invalid
6. **Running commands**: Backend commands (fastapi, pytest) must be run from `packages/api/`

## Agent Playbook

Full workflow rules are in `AGENT_PLAYBOOK.md` at the project root. Read it before starting any issue-driven work.

Key rules (always apply):
- Never push directly to `main` or `dev` — all changes go through PRs targeting `dev`
- Conventional commits required (e.g., `feat(parser): add boilerplate removal`)
- TDD: write tests before implementation (Red → Green → Refactor)
- Follow the layered architecture — routers → services → repositories → models
- Run `pytest`, `ruff check`, and `mypy` before creating PRs
- Branch naming: `feature/<issue-number>-<short-description>` from `dev`
- All plans and issue selections require human approval (Level 1 autonomy)

## Current State

- Monorepo structure with `packages/api/` (backend) and `packages/web/` (frontend)
- Repository pattern for data access
- User model and authentication schemas
- Landing, dashboard, and email detail pages
- Modern SPA with API backend
