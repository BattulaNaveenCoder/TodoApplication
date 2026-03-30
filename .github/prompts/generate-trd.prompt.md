# Generate TRD Prompt

Create a Technical Requirements Document for implementing an approved PRD item.

## Required Output Sections
1. Technical Overview
2. Architecture Impact
3. API Contract Changes
4. Data Model and Migration Plan
5. Validation and Error Handling
6. Test Strategy
7. Rollout Plan
8. Monitoring and Logging
9. Risks and Mitigations
10. Definition of Done

## Project Context
- Backend layering: Router -> Service -> Repository
- ORM only; no raw SQL
- Frontend calls backend via typed API modules
- Tests required for every new function/path

## Rules
- Include file-level impact summary.
- Keep compatibility notes for existing endpoints/components.
- Include concrete acceptance criteria.
