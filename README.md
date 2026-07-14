# Mail2Audio

Convert email newsletters into audio clips using Amazon Polly TTS. Upload `.eml` files or link a Gmail account to generate audio from subscribed newsletters.

## Tech Stack

- **Backend:** FastAPI + SQLAlchemy (Python)
- **Frontend:** React 19 + TypeScript + Vite
- **Database:** SQLite (development)
- **TTS:** Amazon Polly (planned)

## Project Structure

```
packages/
├── api/          ← FastAPI backend (routers → services → repositories → models)
│   ├── app/
│   ├── tests/
│   └── pyproject.toml
└── web/          ← React frontend
    └── src/
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+

### Install dependencies

```bash
# Python (from project root, using a virtual environment)
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

## Branching Strategy

This project uses **Git Flow**:

- `main` — production-ready, tagged releases only
- `dev` — integration branch, all feature work merges here
- `feature/<issue>-<description>` — short-lived branches from `dev`

Both `main` and `dev` are protected — all changes require Pull Requests.

## Contributing

See [`AGENT_PLAYBOOK.md`](AGENT_PLAYBOOK.md) for workflow rules, commit conventions, and coding standards.
