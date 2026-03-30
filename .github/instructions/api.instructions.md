---
applyTo: "backend/**/*.py,backend/alembic/**/*.py"
---

# API Instructions

- Keep strict Route -> Service -> Repository boundaries.
- Routers handle HTTP only and never import repositories directly.
- Services contain business rules and never access the database directly.
- Repositories contain data access only and never raise HTTP exceptions.
- Use SQLAlchemy 2.x synchronous sessions and select() queries.
- Validate all request inputs with Pydantic schemas at router boundaries.
- Raise domain exceptions in services; map them to HTTP errors in routers.
- Add Google-style docstrings and full type hints to public functions.
- Keep functions focused and under 40 lines when practical.
- Add or update tests for each changed public function.
