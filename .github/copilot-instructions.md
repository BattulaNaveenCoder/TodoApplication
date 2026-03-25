# Copilot instructions — Todo App (shared)

Stack: React + TypeScript frontend, Python FastAPI backend,
SQL Server Express via SQLAlchemy + Alembic. Single user, no auth.

## Architecture
- Strict Route -> Service -> Repository layering. No exceptions.
- No business logic in routers.
- No direct DB access in services.
- Routers never import repositories directly.

## Code quality
- All public functions must have docstrings.
- No magic numbers — use named constants or config values.
- No commented-out code in commits.
- Functions must do one thing. Max 40 lines per function.

## Error handling
- Never swallow exceptions silently.
- Always return meaningful error messages.
- Use custom exception classes, not generic Exception.
- HTTP errors must include error code + human-readable message.

## Testing
- Every new function needs a corresponding unit test.
- Test file mirrors source file structure.
- Tests must be independent — no shared mutable state.
- Test names: test_<what>_when_<condition>

## Git workflow
- Feature branches only — never commit to main directly.
- Branch naming: feature/<short-description>
- Commit format: <type>(<scope>): <description>
- Types: feat, fix, test, refactor, docs, chore
- PRs require passing tests before merge.

## Security
- No secrets or credentials in code.
- All config from environment variables via .env.
- Validate all inputs at router layer via Pydantic.
- No raw SQL — always use ORM.

## Documentation
- Every module must have a module-level docstring.
- API endpoints must document: purpose, params, responses, errors.
- Keep README up to date with setup steps.
