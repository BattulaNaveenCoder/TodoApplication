---
applyTo: "frontend/src/**/*.{ts,tsx}"
---

# Web Instructions

- Use React functional components and hooks only.
- Keep API calls in frontend/src/api and business UI state in hooks.
- Use strict TypeScript types; do not use any.
- Name props interfaces as <ComponentName>Props.
- Keep components presentation-focused and move API concerns to hooks.
- Handle loading, error, empty, and success states explicitly.
- Use accessible labels for form controls and explicit button types.
- Keep styling consistent with existing project patterns.
- Add or update Vitest + React Testing Library tests for behavior changes.
