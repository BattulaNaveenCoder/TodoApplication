# DB Migration Prompt

Task:
Generate and review an Alembic migration for schema changes in backend/app/models.

Checklist:
1. Confirm model imports are wired in backend/alembic/env.py.
2. Generate migration name in snake_case.
3. Inspect autogeneration output for unintended changes.
4. Verify constraints, indexes, nullability, and foreign keys.
5. Ensure downgrade is safe and reversible.

Output:
- Recommended terminal commands.
- Migration review notes (what changed and why).
- Any required manual edits to the generated migration.
