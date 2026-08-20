# Mail2Audio

Convert email newsletters into audio clips using Amazon Polly TTS. Upload `.eml` files or link a Gmail account to generate audio from subscribed newsletters.

## Project status

_Last reviewed: 2026-08-20._

| Module | State | Notes |
|---|---|---|
| `packages/web` | **Working** | React 19 + TypeScript on Vite. Landing, Dashboard and EmailDetail pages build clean. |
| `packages/api` | **Partly broken** | Email parsing is solid; the HTTP layer around it is not. See below. |
| `infrastructure` | **Skeleton** | Terraform is provider config only, Ansible is a connectivity check. No resources defined. |
| TTS (Amazon Polly) | **Not started** | `boto3` is a declared dependency with no call sites. No audio model, endpoint or storage yet. |

### What works today

- **`.eml` parsing.** `EmailParser` extracts subject/sender/recipient/date and flattens newsletter HTML
  to clean text, correctly skipping `<script>` and `<style>`.
- `GET /health` and `GET /api/emails/` respond correctly.
- The frontend builds (`npm run build`) and runs against the Vite dev proxy.

### What's broken today

- **Uploading an email fails.** `POST /api/emails/upload` returns
  `500 TypeError: Expected bytes or str, got UploadFile` — the router hands the file object to a service
  that expects bytes. This is the core flow and the next thing to fix.
- **Two backend test modules don't run.** `pytest` reports `9 passed, 2 errors`; both errors are import
  failures at collection, not assertion failures.
- **Response schemas don't line up.** The service returns a schema without `id`, the routes declare one
  with it, and the frontend expects fields (`has_audio`, `body_text`) the API never sends.
- **Gmail OAuth is not wired up.** The OAuth client is fully written but nothing calls it; `routers/auth.py`
  is TODO stubs and stays commented out of `main.py`.
- **`ruff` and `mypy` are required by the playbook but not installed or configured**, so that pre-PR gate
  has never actually run.

Exact reproduction details for each item are in [`CLAUDE.md`](CLAUDE.md) under "Known-Broken / In-Progress".

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy (Python)
- **Frontend:** React 19 + TypeScript + Vite
- **Database:** SQLite (development)
- **TTS:** Amazon Polly (planned)

## Project Structure

```
packages/
├── api/            ← FastAPI backend (routers → services → repositories → models)
│   ├── app/
│   ├── tests/
│   └── pyproject.toml
└── web/            ← React frontend (Vite + TypeScript)
    └── src/
infrastructure/     ← Terraform (AWS) and Ansible scaffolding
docs/               ← sample .eml newsletters used as test fixtures
```

`packages/web/` and `infrastructure/` each carry their own `CLAUDE.md` with module-specific notes.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+

### Install dependencies

```bash
# Python — the virtualenv lives at the REPO ROOT, not in packages/api/
python3 -m venv venv          # first time only
source venv/bin/activate
pip install -e "packages/api[dev]"

# Node (installs root + web workspace)
npm install
```

### Run development servers

```bash
# Start both API (:8000) and frontend (:5173) concurrently
npm run dev
```

### Run tests

```bash
cd packages/api && pytest -v
```

Backend commands must run from `packages/api/` — imports and the SQLite path resolve relative to it.
Two modules currently fail to collect (see [Project status](#project-status)), so a clean run today is
`9 passed, 2 errors` until those are fixed.

## Branching Strategy

This project uses **Git Flow**:

- `main` — production-ready, tagged releases only
- `dev` — integration branch, all feature work merges here
- `feature/<issue>-<description>` — short-lived branches from `dev`

Both `main` and `dev` are protected — all changes require Pull Requests.

## Contributing

See [`AGENT_PLAYBOOK.md`](AGENT_PLAYBOOK.md) for workflow rules, commit conventions, and coding standards.
