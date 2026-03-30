Role:
You are a Senior Product Manager with 15+ years of experience writing
PRDs for enterprise web applications.

Task:
Generate a comprehensive Product Requirements Document (PRD) for a
full-stack Todo Management Application covering Phase 1 (Todo only)
and Phase 2 (Todo with Categories).

Audience:
Developers, architects, and QA engineers who will use this PRD to
build the application and derive a Technical Requirements Document.

Context:
- Full-stack single-user application, no authentication required
- Frontend: React 18 with Tailwind CSS
- Backend: Python FastAPI
- Database: SQL Server Express running locally, Windows Authentication
- ORM: SQLAlchemy with Alembic for migrations
- Architecture: Route → Service → Repository pattern
- Phase 1: Complete Todo CRUD operations
- Phase 2: Add Category management and link Todos to Categories
- The guide is for learning AI-assisted enterprise development

Constraints:
- No authentication, no multi-user support
- Application runs entirely on local developer machine
- All features must be fully testable
- Enterprise standards for code quality, documentation, and error handling
- No external third-party service integrations

Output:
Create the file docs/PRD.md with these sections:
1. Executive Summary
2. Goals and Objectives
3. Scope — In-scope and Out-of-scope for both phases
4. User Stories (As a user I want... so that...)
	Phase 1: Create, view, update, delete, complete, uncomplete a todo
	Phase 2: Create/edit/delete categories, assign category to todo,
				filter todos by category
5. Functional Requirements — numbered, grouped by feature area
6. Non-Functional Requirements — performance, reliability,
	maintainability, documentation standards
7. Data Model description — entities, fields, types, constraints
	(descriptive prose, no SQL)
8. API Endpoints — HTTP method, path, request body, response shape
	for both phases
9. Error Handling Requirements
10. Acceptance Criteria per user story
11. Out of Scope for v1.0
