Role:
You are a Solutions Architect with 20+ years of experience designing
enterprise-grade full-stack systems.

Task:
Generate a Technical Requirements Document (TRD) based on the PRD
at docs/PRD.md.

Audience:
Senior and mid-level developers implementing the system in Python
FastAPI, React, SQLAlchemy, Alembic, and SQL Server Express.

Context:
- Read docs/PRD.md fully before writing the TRD
- Windows Authentication for SQL Server (no username/password in code)
- Connection string loaded from .env file via python-dotenv
- SQLAlchemy 2.x synchronous (not async) — simpler for SQL Server
  on Windows with pyodbc
- Pydantic v2 for all request/response schemas
- pytest with SQLite in-memory database for all tests
  (isolates tests from SQL Server dependency)
- React 18 + Vite + TypeScript + Tailwind CSS
- Frontend woven in from the start, not added at the end

Constraints:
- Strict Route → Service → Repository layering — no exceptions
- All Python code must use type hints throughout
- All public functions must have Google-style docstrings
- Alembic handles all schema changes — no manual SQL
- Tests never connect to SQL Server — use SQLite in-memory only
- Connection string must never be hardcoded

Output:
Create docs/TRD.md with these sections:
1. System Architecture Overview
	- Layer responsibilities and boundaries
	- Full component interaction description
2. Monorepo Folder Structure
	- Complete directory tree for both /backend and /frontend
	- Purpose of every folder explained
3. Backend Technical Specifications
	a. FastAPI app setup — startup, middleware, CORS, exception handlers
	b. SQLAlchemy sync engine, session management, Base model
	c. Alembic configuration for SQL Server + Windows Auth
	d. All model definitions — fields, types, constraints, relationships
	e. Pydantic v2 schemas — request and response with field examples
	f. Repository layer — class structure, method signatures
	g. Service layer — class structure, business rules, exception raising
	h. Router layer — all endpoints, status codes, dependency injection
	i. Custom exception hierarchy
	j. Environment configuration — full .env structure
4. Frontend Technical Specifications
	a. Component tree for Phase 1 and Phase 2
	b. API integration layer (axios, base URL, error handling)
	c. State management via custom hooks
	d. Folder structure
5. Database Design
	- Phase 1 table: todos
	- Phase 2 tables: categories + updated todos with FK
	- Migration strategy for adding category to existing todos
6. Testing Strategy
	- Layers tested and what is tested at each layer
	- conftest.py structure and fixtures
	- SQLite in-memory setup for test isolation
	- Coverage targets per layer
7. Development Workflow
	- Branch naming, commit message format
	- PR checklist
8. Instruction File and Custom Skills Strategy
	- Scope of each instruction file
	- What each custom skill prompt file covers
