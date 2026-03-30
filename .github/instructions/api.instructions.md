---
applyTo: backend/**/*.py
---

# API Instructions (FastAPI + SQLAlchemy)

## Scope
- Applies to backend Python files under `backend/`.
- Follow shared rules in `.github/copilot-instructions.md`.

## Layering Rules
- Router -> Service -> Repository only.
- Routers validate request/response via Pydantic schemas.
- Services own business logic and orchestration.
- Repositories own all ORM data access.

## FastAPI Rules
- Keep route handlers thin.
- Return explicit response models.
- Use dependency injection for DB sessions.
- Raise structured HTTP errors with code + message.

## SQLAlchemy Rules
- Use ORM, never raw SQL.
- Keep transactions explicit and minimal.
- Handle `IntegrityError` and map to domain exceptions.

## Testing Rules
- Add/extend unit tests for every new function.
- Mirror source structure under `backend/tests/`.
- Use deterministic fixtures; avoid shared mutable state.

## Quality Checklist
- Public functions include docstrings.
- No magic numbers.
- Functions should remain focused and short.
- Remove dead or commented-out code before commit.
