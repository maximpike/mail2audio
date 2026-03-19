# Mail2Audio — Agent Playbook

> This document defines the rules, workflow, and standards that any agent working on the
> Mail2Audio repository must follow. It is version-controlled alongside the code.

---

## 1. Branching Strategy: Git Flow

```
main          ← production-ready, tagged releases only
  ↑
dev           ← integration branch, all feature work merges here first
  ↑
feature/*     ← short-lived branches for individual issues
release/*     ← release preparation branches (cut from dev)
hotfix/*      ← emergency fixes branching from main
```

### Branch Naming Conventions

| Branch Type | Format | Example |
|-------------|--------|---------|
| Feature | `feature/<issue-number>-<short-description>` | `feature/42-tts-interface` |
| Bugfix | `bugfix/<issue-number>-<short-description>` | `bugfix/55-date-parse-error` |
| Release | `release/<version>` | `release/0.2.0` |
| Hotfix | `hotfix/<issue-number>-<short-description>` | `hotfix/60-auth-token-expiry` |

### Rules

- Feature branches are created from `dev` and merge back into `dev`.
- Release branches are cut from `dev` when a milestone is ready. Only bugfixes go into a release branch. When ready, the release branch merges into both `main` and `dev`, and `main` is tagged.
- Hotfix branches are created from `main` for urgent production fixes. They merge into both `main` and `dev`.
- Never push directly to `main` or `dev`. All changes go through Pull Requests.
- Delete feature branches after merge.

---

## 2. Agent Workflow (Step by Step)

### Phase 1: Issue Selection (Requires Human Approval)

1. Review the GitHub project board for issues in the "Backlog" or "Ready" column.
2. Propose an issue to the human operator, including:
   - Issue number and title
   - Why this issue should be next (dependencies, priority, milestone alignment)
   - Estimated scope (files affected, tests needed)
3. **Wait for human approval before proceeding.**

### Phase 2: Planning (Requires Human Approval)

1. Write an implementation plan covering:
   - Files to create or modify
   - New tests to write (tests FIRST — this is TDD)
   - Dependencies or packages needed
   - Any architectural decisions or trade-offs
2. **Wait for human approval of the plan before writing code.**

### Phase 3: Implementation

1. Create the feature branch from `dev`:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/<issue-number>-<short-description>
   ```
2. Write tests first (Red phase of TDD).
3. Implement the minimum code to make tests pass (Green phase).
4. Refactor if needed (Refactor phase).
5. Run the full test suite and confirm all tests pass.
6. Run linting (`ruff check` and `ruff format --check`).
7. Run type checking (`mypy app/`).
8. Commit with conventional commit messages (see Section 4).

### Phase 4: Pull Request (Requires Human Review)

1. Push the feature branch to origin.
2. Create a Pull Request targeting `dev`.
3. PR title format: `feat: <description> (#<issue-number>)`
4. PR description must include:
   - Summary of changes
   - List of files changed
   - How to test (manual steps if applicable)
   - Link to the GitHub issue
   - Checklist:
     ```
     - [ ] All tests pass
     - [ ] Linting passes (ruff)
     - [ ] Type checking passes (mypy)
     - [ ] No new warnings
     - [ ] Conventional commit messages used
     ```
5. **Wait for human review.** Address any requested changes.

### Phase 5: Merge & Cleanup

1. Once approved, the **human merges the PR** into `dev`.
2. The human tests on `dev`.
3. When a milestone is complete, the human cuts a release branch and merges to `main`.
4. The agent deletes the feature branch after merge.

### GitHub Issue Updates

The agent should update issues at each phase:

| Event | Issue Update |
|-------|-------------|
| Issue selected and approved | Move to "In Progress", add comment with implementation plan |
| PR created | Add comment linking to the PR |
| PR merged | Move to "Done", close the issue |
| Blocked or questions arise | Add comment describing the blocker |

---

## 3. Architecture Rules

### Layered Architecture (Mandatory)

All code must follow the established layered architecture:

```
Routers (app/routers/)      → HTTP endpoints, request/response handling only
    ↓
Services (app/services/)    → Business logic, orchestration
    ↓
Repositories (app/repositories/) → Data access, CRUD operations
    ↓
Models (app/models/)        → SQLAlchemy ORM entities
Schemas (app/schemas/)      → Pydantic DTOs for validation
```

**Rules:**
- Routers never access repositories directly — always go through a service.
- Services never import from routers.
- Repositories handle only database operations — no business logic.
- Schemas are used at API boundaries for validation. Models are internal.
- New layers require human approval before implementation.

### Frontend Architecture

```
packages/web/src/
├── components/    → Reusable UI components
├── pages/         → Route-level page components
├── hooks/         → Custom React hooks for state/logic
├── services/      → API client functions
├── types/         → TypeScript interfaces and types
└── styles/        → CSS files (one per page/component)
```

**Rules:**
- Components must be functional (no class components).
- All props must have TypeScript interfaces.
- API calls live in `services/`, not in components.
- State management through hooks, not prop drilling beyond 2 levels.

---

## 4. Commit Standards

### Conventional Commits (Required)

Every commit message must follow this format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer with issue reference]
```

**Types:**

| Type | When to Use |
|------|------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `refactor` | Code restructuring without behaviour change |
| `test` | Adding or updating tests only |
| `docs` | Documentation changes only |
| `chore` | Build, config, tooling changes |
| `style` | Code formatting (no logic change) |

**Scope** (optional but encouraged): `parser`, `auth`, `tts`, `frontend`, `api`, `db`, `ci`

**Examples:**
```
feat(parser): add boilerplate removal for newsletter footers
test(repository): add edge case for nonexistent email ID
fix(auth): handle expired refresh token gracefully
chore: add ruff and mypy configuration to pyproject.toml
docs: update README with development setup instructions
```

**Rules:**
- Subject line ≤ 72 characters.
- Use imperative mood ("add", "fix", "update" — not "added", "fixes", "updated").
- One logical change per commit. Don't bundle unrelated changes.
- Reference the issue number in the footer: `Closes #42` or `Refs #42`.

---

## 5. Testing Standards

### TDD Is Mandatory

The agent must write tests before implementation. The workflow is:

1. **Red** — Write a failing test that defines the expected behaviour.
2. **Green** — Write the minimum code to make the test pass.
3. **Refactor** — Clean up while keeping tests green.

### Test Organisation

```
packages/api/tests/
├── conftest.py                    → Root fixtures (TestClient, sample HTML)
├── test_repositories/
│   ├── conftest.py                → DB fixtures (in-memory SQLite)
│   └── test_<entity>_repository.py
├── test_services/
│   ├── conftest.py                → Mocks, .eml file fixtures
│   └── test_<service_name>.py
└── test_routers/
    ├── conftest.py                → API test fixtures
    └── test_<router_name>.py
```

### Test Naming

```python
def test_<what_is_being_tested>_<expected_outcome>():
    """Descriptive docstring of the test scenario"""
```

Example: `test_parse_none_date_returns_none()`

### Test Structure (AAA Pattern)

Every test must follow Arrange-Act-Assert:

```python
def test_example(self):
    # Arrange — set up test data and dependencies
    email_data = {...}

    # Act — call the method under test
    result = service.process(email_data)

    # Assert — verify the expected outcome
    assert result.id is not None
```

### Coverage Requirements

- All new code must have corresponding tests.
- Run `pytest --cov=app --cov-report=term-missing` before raising a PR.
- Target: 80%+ line coverage on new code.

### Pre-PR Test Checklist

Before creating a Pull Request, the agent must run and confirm:

```bash
cd packages/api

# All tests pass
pytest -v

# Coverage report
pytest --cov=app --cov-report=term-missing

# Linting
ruff check app/ tests/

# Formatting
ruff format --check app/ tests/

# Type checking
mypy app/
```

All must pass with zero errors.

---

## 6. Code Quality Standards

### Python

- **Type hints on all function signatures** (parameters and return types).
- **Docstrings on all public methods** — describe purpose, args, and return values.
- **No `# noqa` or `# type: ignore`** without an explanatory comment.
- **No `print()` statements** — use `logging` module if debug output is needed.
- **No wildcard imports** (`from module import *`).
- **Explicit is better than implicit** — avoid magic, be readable.

### TypeScript

- **No `any` type** unless absolutely unavoidable (with comment explaining why).
- **Interfaces over type aliases** for object shapes.
- **Named exports preferred** over default exports (except for page components).

### Both

- **Max file length: 300 lines.** If a file exceeds this, consider splitting.
- **Max function length: 30 lines.** If a function exceeds this, extract helpers.
- **DRY but not at the cost of readability.** A little duplication is better than premature abstraction.

---

## 7. Autonomy Levels

The agent's autonomy will increase over time as trust is established.

### Level 1: Full Human Control (Current)

| Step | Agent Action | Human Action |
|------|-------------|-------------|
| Issue selection | Proposes | Approves |
| Implementation plan | Writes plan | Approves |
| Code implementation | Writes code | — |
| Test execution | Runs tests | — |
| PR creation | Creates PR | Reviews and merges |
| Issue updates | Updates issues | — |
| Merge to dev | — | Merges |
| Merge to main | — | Merges |

### Level 2: Trusted Implementation (Future)

- Agent selects from pre-approved issue backlog without per-issue approval.
- Agent implements and creates PR without plan approval.
- Human still reviews all PRs and handles merges.

### Level 3: Semi-Autonomous (Future)

- Agent can merge to dev after automated checks pass.
- Human reviews only for merge to main.
- Agent can create new issues for discovered bugs or tech debt.

---

## 8. What the Agent Must Never Do

- Push directly to `main` or `dev`.
- Merge its own Pull Requests.
- Delete or modify existing tests without human approval.
- Change the database schema without human approval.
- Add new dependencies without documenting why in the PR.
- Suppress linting or type-checking errors.
- Commit secrets, tokens, API keys, or credentials.
- Modify this playbook without human approval.
