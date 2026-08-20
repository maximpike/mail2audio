# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mail2Audio converts email newsletters into audio clips using Amazon Polly TTS. Users upload `.eml`
files or link a Gmail account. The email parsing pipeline is the part currently under construction —
**TTS/audio generation does not exist yet**: `boto3` is a declared dependency but has no call sites,
and there is no audio model, endpoint, or storage.

## Environment

The Python virtualenv lives at the **repo root** (`venv/`, Python 3.13), not inside `packages/api/`.
Activate it before any backend command:

```bash
source venv/bin/activate     # from repo root, before any backend command
```

Backend commands (`fastapi`, `pytest`) must run **from `packages/api/`** — imports and the SQLite
path resolve relative to that directory.

## Build/test baselines

`npm run dev` starts both servers. Backend tests are the only test suite — the frontend has none.

- **`pytest` runs no coverage by default** (no coverage config in `pyproject.toml`). `pytest-cov` *is*
  installed but undeclared in the dev extras, so `pytest --cov=app --cov-report=term-missing` works.
- **`npm run lint` currently exits 1** on a pre-existing error (see Known-Broken); `npm run build` is clean.
  A red lint run is not necessarily your change — check the reported file first.

`ruff` and `mypy` are **not installed and not configured**, despite `AGENT_PLAYBOOK.md` §5 requiring
both pre-PR. Adding them to `packages/api/pyproject.toml` `[project.optional-dependencies].dev` is
outstanding work — don't report those checks as passing when they never ran.

## Architecture

### Backend (`packages/api/app/`)

Layering is `routers → services → repositories → models`. Routers must never reach past services into
repositories. Full rules in `AGENT_PLAYBOOK.md` §3.

**Dependency injection is FastAPI `Depends()` all the way down.** `EmailRepository.__init__` takes
`db: Session = Depends(get_db)`, `EmailService.__init__` takes `email_repo: EmailRepository = Depends()`,
and routers take `email_service: EmailService = Depends()`. FastAPI resolves the entire chain from the
route signature — instantiating these classes outside a request means constructing collaborators by hand.

**Package wiring:** `app/models/__init__.py` re-exports `Base` and `Email`; `app/db/__init__.py`
re-exports `engine`, `SessionLocal`, `get_db`; `app/schemas/__init__.py` re-exports the email schemas.
Import from the package (`from app.models import Email`), matching existing code.

**Absolute `app.`-prefixed imports are mandatory.** Both the app and pytest run with `packages/api/` as
the working directory, so `from services.x import Y` raises `ModuleNotFoundError`. This is precisely why
`app/routers/auth.py` is commented out of `main.py` — it imports `from auth.gmail_oauth_client import ...`
and `from config import ...`, neither of which resolves. Fixing those two lines is a prerequisite to
enabling the auth router.

**Table creation:** `Base.metadata.create_all(bind=engine)` runs at import time in `app/main.py`. There
are no migrations, so any model change requires deleting `packages/api/mail2audio.db` and restarting.
Alembic is present in the venv but never initialised.

### Email pipeline

`routers/emails.py` → `EmailService.process_file()` → `EmailParser.parse_eml_file()` → `EmailRepository.create()`

`EmailParser` extracts the **`text/html` part only**, so a plain-text-only email yields `body = None`.
Dates return `None` on any parse failure. `EmailService.process_file()` rejects emails missing
`subject` or `sender`.

Package-specific notes live in `packages/web/CLAUDE.md` and `infrastructure/CLAUDE.md`; they load
automatically when you work in those trees.

## Known-Broken / In-Progress

Do not treat these as working code to build on:

- **Two test modules fail at collection.** `tests/test_repositories/test_email_repository.py` imports
  `EmailCreate` from `app.schemas.email` — a schema that was never written; `tests/test_services/test_email_service.py`
  uses a non-`app.`-prefixed import. Current baseline is `9 passed, 2 errors`.
- **The upload route is miswired.** `routers/emails.py` reads `content = await file.read()`, calls
  `EmailParser.parse_eml_file(content)`, discards the result, then calls `email_service.process_file(file)`
  — passing the `UploadFile` where `process_file` type-checks for `bytes` and raises `TypeError`.
- **Schema mismatches.** `EmailService` returns `EmailBase`, which lacks `id`/`received_at`/`created_at`
  and has no `from_attributes=True`, while routers declare `response_model=EmailResponse`. `EmailBase`
  also uses `minlength=`, silently ignored by Pydantic v2 (correct key: `min_length`) — this is the source
  of the deprecation warnings in every test run. The frontend `types/email.ts` expects `has_audio`,
  `body_html`, and `body_text`, none of which the backend returns.
- **Frontend lint is red.** `hooks/useEmailUpload.ts:25` binds `err` in a `catch` and never uses it,
  tripping `@typescript-eslint/no-unused-vars`. One error, and the only one — fix it and the suite is green.
- **Empty files:** `models/user_model.py`, `repositories/user_repo.py`, `schemas/auth_schema.py`.
  No `User` model exists, so `Email` has no owner FK.
- **Auth:** `auth/gmail_oauth_client.py` is fully implemented (authorization URL, code exchange, token
  persisted to `tokens/gmail_token.json` at chmod 600) but nothing calls it; `routers/auth.py` is TODO stubs.

## Conventions

- `app/config.py` holds Gmail OAuth constants as plain module-level strings — no env-var loading exists.
  `.env/` is a gitignored *directory* of local secrets, not a dotenv file.
- `db/database.py` sets `echo=True`, so dev and test output is flooded with SQL. Test engines pass
  `echo=False`.
- `.gitignore` is deliberately split: the root file holds cross-cutting rules only, with tool-specific
  ignores in `packages/api/`, `packages/web/`, and `infrastructure/terraform/`. Add new ignores to the
  nearest nested file.
- Test fixtures are layered: `tests/conftest.py` (`test_app`, `client`, `sample_email_html`),
  `test_repositories/conftest.py` (in-memory SQLite `test_engine`/`test_db`, sample data), and
  `test_services/conftest.py` (mocked repo/parser plus real `.eml` fixtures resolved from
  `docs/email-examples/` via `Path(__file__).resolve().parents[4]` — that hop count breaks if tests move).
- `email_parser.py` still contains debug `print()` calls, which the playbook forbids.

## Agent Workflow

`AGENT_PLAYBOOK.md` at the repo root is binding — read it before starting issue-driven work. Highlights:

- Never push to `main` or `dev` (both are protected); branch `feature/<issue-number>-<desc>` from `dev`
  and PR back into `dev`.
- Level 1 autonomy: issue selection **and** the implementation plan each require human approval before
  any code is written.
- TDD is mandatory (Red → Green → Refactor). Conventional commits, subject ≤ 72 chars, imperative mood.
- Max 300 lines per file, 30 lines per function; type hints and docstrings on all public Python methods.
