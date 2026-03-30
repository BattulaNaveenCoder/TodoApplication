# Commit Message Prompt

Generate a commit message from the current staged changes.

## Format
`<type>(<scope>): <description>`

## Allowed Types
- feat
- fix
- test
- refactor
- docs
- chore

## Rules
- Use present tense and imperative mood.
- Keep subject line <= 72 chars.
- Scope should be one of: api, web, db, tests, docs, build.
- Add a short body only when needed for context.

## Example
`fix(api): handle missing todo id with 404 response`
