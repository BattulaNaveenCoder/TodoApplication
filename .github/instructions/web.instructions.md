---
applyTo: frontend/**/*.{ts,tsx,css}
---

# Web Instructions (React + TypeScript + Vite)

## Scope
- Applies to frontend files under `frontend/`.
- Follow shared rules in `.github/copilot-instructions.md`.

## Frontend Architecture
- UI components in `components/` are presentational.
- Page-level composition stays in `pages/`.
- Data-fetching and state orchestration stays in hooks.
- API calls go through `api/` modules only.

## TypeScript Rules
- Prefer explicit shared types from `types/`.
- Avoid `any`; use precise unions/interfaces.
- Keep components small and focused.

## UX and State Rules
- Handle loading, error, empty, and success states.
- Preserve optimistic updates only with rollback paths.
- Show user-friendly error messages.

## Testing Rules
- Add/extend tests for changed components/hooks.
- Prefer behaviour-focused tests with Testing Library.
- Mock network calls at API module boundaries.

## Quality Checklist
- No dead code or commented-out logic.
- Keep styles consistent and scoped.
- Validate forms before sending requests.
