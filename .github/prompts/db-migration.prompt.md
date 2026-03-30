# DB Migration Prompt

Generate and review an Alembic migration for backend schema changes.

## Required Tasks
1. Summarize model changes and migration intent.
2. Generate migration script with explicit upgrade/downgrade logic.
3. Verify naming clarity for tables, constraints, and indexes.
4. Check backward compatibility and data safety.
5. Provide rollback notes and validation steps.

## Project Rules
- Use SQLAlchemy ORM models as source of truth.
- Keep migration scripts deterministic and reversible.
- Avoid destructive actions without mitigation.
- Match SQL Server compatibility requirements.

## Output Requirements
- List impacted files.
- Include migration test/verification commands.
- Highlight any manual data backfill steps if required.
