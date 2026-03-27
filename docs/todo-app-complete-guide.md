# Todo App — AI-First Enterprise Development Guide
## Complete Step-by-Step Guide with GitHub Copilot & VS Code

> **Purpose:** A complete, prompt-driven guide to build a full-stack Todo
> application using GitHub Copilot Agent Mode. No manual coding — everything
> generated through structured AI prompts following the
> Role/Task/Audience/Context/Constraints/Output pattern.

---

## Table of Contents

- [Tech Stack & Decisions](#tech-stack--decisions)
- [Phase 0: Project Foundation & Scaffolding](#phase-0-project-foundation--scaffolding)
- [Phase 1: Basic Todo — Full Stack (Steps 1 & 2)](#phase-1-basic-todo--full-stack-steps-1--2)
- [Phase 2: Unit Tests (Steps 3 & 4)](#phase-2-unit-tests-steps-3--4)
- [Phase 3: Add Category (Steps 5 & 6)](#phase-3-add-category-steps-5--6)
- [Phase 4: Edge Cases & Hardening (Steps 7, 8 & 9)](#phase-4-edge-cases--hardening-steps-7-8--9)
- [Phase 5: Final Polish & Wrap-up (Step 10)](#phase-5-final-polish--wrap-up-step-10)
- [Quick Reference](#quick-reference--all-prompts-and-commands)

---

## Tech Stack & Decisions

| Area | Decision |
|---|---|
| Frontend | React 18 + Vite + TypeScript + Tailwind CSS |
| Backend | Python 3.11+ FastAPI |
| Database | SQL Server Express, Windows Authentication |
| ORM | SQLAlchemy 2.x synchronous + Alembic |
| Architecture | Route → Service → Repository (strict) |
| Validation | Pydantic v2 |
| Testing (backend) | pytest + SQLite in-memory (no SQL Server in tests) |
| Testing (frontend) | Vitest + React Testing Library |
| Repo structure | Monorepo: /backend and /frontend |
| Git flow | feature/* → main via Pull Request |
| Copilot mode | Agent mode in VS Code Chat window |
| Custom skills | .github/prompts/*.prompt.md (invoked with #skill-name) |

---

## Phase 0: Project Foundation & Scaffolding

---

### 0.1 — Prerequisites Checklist

Before running any prompt, confirm these are in place:

```
Local machine:
  ✓ VS Code with GitHub Copilot extension installed
  ✓ Copilot Chat enabled with Agent mode
  ✓ Python 3.11+ installed
  ✓ Node.js 18+ installed
  ✓ SQL Server Express installed and running
  ✓ ODBC Driver 17 for SQL Server installed
  ✓ Git installed and configured
  ✓ GitHub account with a new empty repo created (e.g. todo-app)
  ✓ GitHub CLI (gh) installed (optional but recommended)

VS Code extensions to install:
  ✓ GitHub Copilot
  ✓ GitHub Copilot Chat
  ✓ Python (Microsoft)
  ✓ Pylance
  ✓ ESLint
  ✓ Prettier
```

---

### 0.2 — Initialize Local Repo

Run these commands in your terminal before opening VS Code:

```bash
mkdir todo-app
cd todo-app
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/todo-app.git

# Create base folder structure manually (only this once)
mkdir -p .github/prompts
mkdir -p docs
mkdir -p backend
mkdir -p frontend

# Create a placeholder so git tracks folders
touch .github/.gitkeep
touch docs/.gitkeep

# Initial commit
echo "# Todo App" > README.md
git add .
git commit -m "chore(init): initialize repository"
git push -u origin main
```

Now open the `todo-app` folder in VS Code:

```bash
code .
```

---

### 0.3 — Prompt: Generate PRD

Open Copilot Chat → select **Agent mode** → paste:

```
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
```

After Copilot creates `docs/PRD.md`, review it then commit:

```bash
git add docs/PRD.md
git commit -m "docs(prd): add product requirements document"
git push
```

---

### 0.4 — Prompt: Generate TRD

```
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
```

```bash
git add docs/TRD.md
git commit -m "docs(trd): add technical requirements document"
git push
```

---

### 0.5 — Prompt: Shared Copilot Instruction File

```
Role:
You are a Senior Engineering Lead enforcing consistent standards
across a full-stack development team.

Task:
Create the shared GitHub Copilot instruction file that applies
to ALL code in this project — frontend and backend.

Audience:
GitHub Copilot Chat Agent, which reads this file automatically
before responding to any prompt in this workspace.

Context:
- Read docs/TRD.md before generating this file
- Project: full-stack Todo app, React + FastAPI + SQL Server
- Architecture: Route → Service → Repository
- Standards: enterprise-grade, typed, documented, tested

Constraints:
- Instructions must be concise directives — no explanations
- Cover all layers and both languages
- Rules must be unambiguous and actionable
- No duplication between this file and the language-specific files

Output:
Create .github/copilot-instructions.md with these sections:

## Project overview
One paragraph: stack, pattern, purpose, single-user local app.

## Architecture rules
- Strict Route → Service → Repository — no layer skipping
- Routers handle HTTP only — no business logic
- Services hold all business logic — no direct DB access
- Repositories handle all DB access — no HTTP concerns
- No circular imports between layers

## Code quality
- All public functions and classes must have docstrings
- No magic numbers — use named constants
- No commented-out code committed to any branch
- Functions do one thing — max 40 lines
- Meaningful names — no single-letter variables except loop indices

## Error handling
- Never swallow exceptions silently
- Custom exception classes for all domain errors
- HTTP error responses must include: error code + human message
- Never expose stack traces or internal details in API responses

## Testing rules
- Every new function needs a unit test
- Test file mirrors source file path and name
- Tests are independent — no shared mutable state between tests
- Naming: test_<what>_when_<condition> (Python)
         should <do something> when <condition> (React)

## Git workflow
- Feature branches only — never commit directly to main
- Branch format: feature/<short-description>
- Commit format: <type>(<scope>): <description>
  Types: feat, fix, test, refactor, docs, chore
- PRs must have passing tests before merge

## Security hygiene
- No credentials, secrets, or tokens in source code
- All configuration from .env via python-dotenv
- All API inputs validated via Pydantic schemas before use
- No raw SQL queries — SQLAlchemy ORM only
- .env must be in .gitignore and never committed

## Documentation
- Every module must have a module-level docstring
- README must stay current with setup and run instructions
- API changes must be reflected in docs/PRD.md or docs/TRD.md
```

```bash
git add .github/copilot-instructions.md
git commit -m "docs(copilot): add shared copilot instruction file"
git push
```

---

### 0.6 — Prompt: Backend Instruction File

```
Role:
You are a Senior Python Engineer specialising in FastAPI,
SQLAlchemy, and enterprise Python application design.

Task:
Create the backend-specific Copilot instruction file for
the Python FastAPI backend.

Audience:
GitHub Copilot Chat Agent, read automatically when any backend
Python file is active in the editor.

Context:
- Backend lives in /backend folder
- Python 3.11+, FastAPI, SQLAlchemy 2.x sync, Alembic, Pydantic v2
- SQL Server Express, Windows Authentication, pyodbc driver
- Connection string from .env via python-dotenv
- Testing: pytest with SQLite in-memory, no SQL Server in tests

Constraints:
- Python and FastAPI-specific rules only
- No duplication of shared rules already in
  .github/copilot-instructions.md
- Be prescriptive — exact patterns, not general advice

Output:
Create backend/.copilot-instructions.md with sections:

## Python standards
- Python 3.11+ features where appropriate
- Full type hints on every function, method, and variable declaration
- Pydantic models for all data transfer — never plain dicts
- No **kwargs in any public-facing function signature

## FastAPI patterns
- All routers: APIRouter(prefix="...", tags=["..."])
- All endpoints use explicit response_model
- Dependency injection via Depends() for DB session and services
- Status codes explicit: 200, 201, 204, 400, 404, 409, 422, 500
- Endpoint functions are thin — one line to call service, return result
- Global exception handlers in main.py for all custom exceptions

## SQLAlchemy patterns
- Use SQLAlchemy 2.x declarative style with DeclarativeBase
- Synchronous Session (not async) — SQL Server via pyodbc
- Session created per request via Depends(get_db), always closed
- All queries use select() with Session.execute() — never query()
- Explicit column definitions — never rely on defaults or inference
- Models in backend/app/models/, one file per model

## Alembic workflow
- Never alter database schema manually
- Always: alembic revision --autogenerate -m "describe_change"
  then review migration file, then: alembic upgrade head
- Migration messages use snake_case descriptions
- env.py must import all models so autogenerate detects changes

## Repository layer
- Class named <Model>Repository
- Constructor accepts Session, stores as self.db
- Standard methods: get_by_id, get_all, create, update, delete
- Returns model instance or None — never raises HTTP exceptions
- No business logic of any kind

## Service layer
- Class named <Domain>Service
- Constructor accepts repository instance
- All business rules and validation live here
- Raises custom exceptions from app/exceptions.py
- Never imports HTTPException — that belongs in routers

## Router layer
- File per resource: todos.py, categories.py
- Catches domain exceptions, maps to HTTPException with correct status
- Input always validated by Pydantic schema — never raw dict
- Output always a Pydantic response schema — never raw ORM object

## Docstring format — Google style, always:
def example(self, item_id: int) -> Todo:
    """Retrieve a single todo by ID.

    Args:
        item_id: The primary key of the todo to retrieve.

    Returns:
        The matching Todo ORM instance.

    Raises:
        TodoNotFoundError: When no todo exists with the given ID.
    """

## Testing patterns
- pytest.ini: testpaths = tests, no asyncio needed (sync)
- conftest.py: SQLite in-memory engine, session fixture, client fixture
- Repository tests: use real SQLite session — test actual queries
- Service tests: mock repository with unittest.mock.MagicMock
- Router tests: use FastAPI TestClient with overridden get_db
- Test file names mirror source: app/services/todo_service.py
  → tests/test_todo_service.py
```

```bash
git add backend/.copilot-instructions.md
git commit -m "docs(copilot): add backend-specific instruction file"
git push
```

---

### 0.7 — Prompt: Frontend Instruction File

```
Role:
You are a Senior React Engineer who enforces clean component
architecture and maintainable TypeScript frontend code.

Task:
Create the frontend-specific Copilot instruction file for
the React + Tailwind CSS frontend.

Audience:
GitHub Copilot Chat Agent, read automatically when any frontend
file is active in the editor.

Context:
- Frontend lives in /frontend folder
- React 18 + Vite + TypeScript (strict mode)
- Tailwind CSS for styling — no CSS modules, no styled-components
- Axios for API calls to FastAPI backend on localhost:8000
- No routing library in Phase 1 — single page
- Testing: Vitest + React Testing Library

Constraints:
- React and TypeScript specific rules only
- No duplication of shared rules from .github/copilot-instructions.md

Output:
Create frontend/.copilot-instructions.md with sections:

## TypeScript standards
- Strict mode on in tsconfig.json — noImplicitAny, strictNullChecks
- No use of type any — use unknown and narrow with type guards
- type keyword for unions and primitives
- interface keyword for object shapes and component props
- All props interfaces named <ComponentName>Props

## React component rules
- Functional components with hooks only — no class components
- One component per file, filename matches component (PascalCase)
- Props destructured in function signature
- No inline arrow functions in JSX event handlers that recreate
  on every render — use useCallback or define outside JSX

## Tailwind CSS rules
- Utility classes only — no custom CSS files
- Responsive classes where appropriate (sm:, md:)
- Reusable style patterns extracted to a component — not copy-pasted
- Dark mode not required for v1

## State management
- useState for local UI state
- useReducer when state shape is complex
- API state (loading, error, data) always in a custom hook
- No prop drilling past two levels — use context if needed

## API integration
- All API functions in frontend/src/api/
- One file per resource: todosApi.ts, categoriesApi.ts
- Shared axios instance in frontend/src/api/client.ts
  with baseURL from import.meta.env.VITE_API_URL
- Every API function typed with explicit return type
- Errors caught at hook level, not component level

## Custom hooks
- Hooks in frontend/src/hooks/
- Named: useTodos, useCategories
- Each hook returns: { data, isLoading, error } plus mutation fns
- Hooks never return raw Axios responses — map to domain types

## Folder structure — follow strictly:
src/
  api/          Axios functions per resource + shared client
  components/   Reusable UI components
  hooks/        Custom React hooks
  pages/        Top-level page components
  types/        TypeScript interfaces and domain types
  utils/        Pure utility functions

## Testing
- Vitest + React Testing Library
- Test behaviour not implementation details
- No snapshot tests
- Mock API with vi.mock() at module level
- Every component tests: renders correctly, loading state,
  error state, data displayed state
- Every hook tested with renderHook() from Testing Library
```

```bash
git add frontend/.copilot-instructions.md
git commit -m "docs(copilot): add frontend-specific instruction file"
git push
```

---

### 0.8 — Prompt: Custom Skill — Test Generation

```
Role:
You are a Senior QA Architect defining reusable test generation
standards for a full-stack enterprise application.

Task:
Create a custom Copilot prompt skill file for generating tests.
This file will be invoked explicitly in Copilot Chat using
#test-generation.

Audience:
GitHub Copilot Chat Agent, invoked by developer when generating
any test file in this project.

Context:
- Backend: pytest, SQLite in-memory, MagicMock for unit tests
- Frontend: Vitest + React Testing Library
- Three test types: repository (real DB), service (mocked repo),
  router/integration (TestClient), component (RTL)
- Test files mirror source file structure
- All tests must be independent and isolated

Constraints:
- This is a prompt file, not an instruction file
- Written as instructions Copilot should follow when invoked
- Must be specific enough that Copilot generates consistent,
  complete test files without further clarification

Output:
Create .github/prompts/test-generation.prompt.md with:

A header: # Test Generation Skill

Then these directives:

When this skill is invoked, always:
1. Read the source file(s) being tested before writing any test
2. Identify: the layer (repository/service/router/component),
   all public methods or endpoints, all possible outcomes
   (success, not found, invalid input, duplicate, etc.)
3. Generate tests for EVERY public method and EVERY outcome
4. Follow naming: test_<what>_when_<condition> (Python)
                  should <do something> when <condition> (React)
5. Structure every test as Arrange / Act / Assert with blank
   line separating each section
6. For repository tests: use real SQLite session from conftest
7. For service tests: mock repository with MagicMock, verify
   repository method calls with assert_called_once_with
8. For router tests: use TestClient, override get_db dependency,
   test status codes AND response body shape
9. For React component tests: mock API module with vi.mock(),
   test each visual state (loading, error, empty, populated)
10. Never test implementation details — test observable behaviour
11. Add a one-line docstring to every test function explaining
    what it verifies
12. Generate conftest.py fixtures if they don't already exist
```

---

### 0.9 — Prompt: Custom Skill — Security Review

```
Role:
You are a Senior Application Security Engineer specialising in
Python web APIs and React frontends.

Task:
Create a custom Copilot prompt skill file for security reviews.
Invoked in Copilot Chat using #security-review.

Audience:
GitHub Copilot Chat Agent, invoked before completing any PR.

Context:
- FastAPI backend with SQLAlchemy ORM, Pydantic validation
- React frontend with Axios
- SQL Server Express, Windows Auth, no JWT or sessions
- Single-user local app — but security hygiene still required

Constraints:
- This is a prompt file invoked explicitly by the developer
- Must produce a structured report with severity levels
- Must cover both backend and frontend files in scope

Output:
Create .github/prompts/security-review.prompt.md with:

A header: # Security Review Skill

Then these directives:

When this skill is invoked, always:
1. Read all files changed in the current feature branch
2. Produce a structured report with sections:

   CRITICAL — must fix before merge:
   - Any raw SQL string concatenation (SQL injection risk)
   - Credentials, API keys, or secrets in source code
   - Stack traces or internal error details exposed in API responses
   - .env file committed to git

   HIGH — should fix before merge:
   - Inputs accepted without Pydantic validation
   - Missing error handling on DB operations
   - CORS configured to allow all origins (*)
   - Unhandled exceptions that could crash the server

   MEDIUM — address in next sprint:
   - Missing rate limiting on write endpoints
   - No input length limits on string fields
   - Console.log statements left in frontend production code

   LOW — best practice suggestions:
   - Functions longer than 40 lines
   - Missing docstrings on public functions
   - Test coverage below 80% on any module

3. For each finding report: severity, file, line number,
   description of risk, specific recommended fix
4. End report with a PASS or NEEDS WORK verdict
```

```bash
git add .github/prompts/
git commit -m "docs(skills): add test-generation and security-review prompt skills"
git push
```

---

### 0.10 — Foundation Complete

Your repository structure at this point:

```
todo-app/
├── .github/
│   ├── copilot-instructions.md
│   └── prompts/
│       ├── test-generation.prompt.md
│       └── security-review.prompt.md
├── docs/
│   ├── PRD.md
│   └── TRD.md
├── backend/
│   └── .copilot-instructions.md
├── frontend/
│   └── .copilot-instructions.md
└── README.md
```

Verify with:

```bash
git log --oneline
# Should show 7 commits on main
```

---

## Phase 1: Basic Todo — Full Stack (Steps 1 & 2)

---

### 1.1 — Create Feature Branch

```bash
git checkout -b feature/basic-todo-api
```

---

### 1.2 — Prompt: Scaffold Backend Project

```
Role:
You are a Senior Python Engineer scaffolding an enterprise FastAPI
application from scratch.

Task:
Scaffold the complete backend project structure with all
configuration files, dependencies, and boilerplate for a
FastAPI + SQLAlchemy + Alembic application.

Audience:
A developer who will then use subsequent prompts to generate
models, schemas, repositories, services, and routers into this
structure.

Context:
- Read docs/TRD.md for the full technical specification
- Backend lives in the /backend folder
- Python 3.11+, FastAPI, SQLAlchemy 2.x synchronous, Alembic
- SQL Server Express, Windows Authentication
  Connection string format:
  mssql+pyodbc://@localhost/TodoDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
- Configuration loaded from backend/.env via python-dotenv
- Read backend/.copilot-instructions.md for all code standards

Constraints:
- Do not generate any models, routes, or business logic yet
- Scaffold only: project structure, config, database setup,
  main app entry point, and empty layer folders with __init__.py
- requirements.txt must pin all versions
- .env.example must be provided (never .env itself)
- .gitignore must exclude .env, __pycache__, .pyc

Output:
Create the following files:

1. backend/requirements.txt
   Include: fastapi, uvicorn[standard], sqlalchemy, pyodbc,
   alembic, pydantic-settings, pydantic[email], python-dotenv,
   pytest, pytest-cov, httpx, requests

2. backend/.env.example
   DATABASE_URL=mssql+pyodbc://@localhost/TodoDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
   APP_ENV=development
   DEBUG=true
   ALLOWED_ORIGINS=http://localhost:5173

3. backend/app/__init__.py (empty with module docstring)

4. backend/app/config.py
   - Settings class using pydantic-settings BaseSettings
   - Reads: DATABASE_URL, APP_ENV, DEBUG, ALLOWED_ORIGINS
   - Singleton get_settings() with lru_cache

5. backend/app/database.py
   - SQLAlchemy engine from DATABASE_URL
   - SessionLocal factory
   - Base = DeclarativeBase()
   - get_db() dependency that yields session, commits on success,
     rolls back on exception, always closes

6. backend/app/exceptions.py
   - AppException base class with message: str and code: str
   - TodoNotFoundError(AppException)
   - DuplicateTitleError(AppException)
   - Comment placeholder for Phase 2 exceptions

7. backend/app/main.py
   - FastAPI app with title, description, version
   - CORS middleware using ALLOWED_ORIGINS from config
   - Global exception handler for AppException → JSON response
   - Health check: GET /health returns {"status": "healthy"}
   - Lifespan context manager (startup log message only for now)

8. backend/app/models/__init__.py (empty with docstring)
9. backend/app/schemas/__init__.py (empty with docstring)
10. backend/app/repositories/__init__.py (empty with docstring)
11. backend/app/services/__init__.py (empty with docstring)
12. backend/app/routers/__init__.py (empty with docstring)
13. backend/tests/__init__.py (empty with docstring)
14. backend/tests/conftest.py (placeholder with TODO comment)
15. backend/alembic.ini (standard Alembic config)
16. backend/alembic/env.py
    - Import Base and all models (placeholder comment)
    - Use DATABASE_URL from config.py
    - Configure for offline and online migrations
```

---

### 1.3 — Prompt: Generate Todo Feature — All Layers

```
Role:
You are a Senior Python Engineer implementing the Todo feature
across all layers of a Route → Service → Repository architecture.

Task:
Generate all backend files for the Todo resource: model, schemas,
repository, service, and router.

Audience:
The development team building this application following the
patterns defined in the instruction files.

Context:
- Read backend/.copilot-instructions.md for all rules
- Read docs/TRD.md for full specifications
- Read backend/app/database.py — use Base and get_db from there
- Read backend/app/exceptions.py — use and extend as needed
- Read backend/app/main.py — register the router here
- Phase 1: No categories yet
- Todo fields: id, title, description, is_completed,
  created_at, updated_at

Constraints:
- Strict layer separation — no cross-layer violations
- Google-style docstrings on every public method and class
- Full type hints throughout
- Repository returns ORM objects or None — never raises HTTP errors
- Service raises domain exceptions — never HTTPException
- Router maps domain exceptions to HTTP responses
- All SQLAlchemy queries use select() with session.execute()
- Response schemas never expose raw ORM objects

Output — generate in this exact order:

1. backend/app/models/todo.py
   Todo model with:
   - id: Integer, primary key, autoincrement
   - title: String(200), not nullable
   - description: String(1000), nullable
   - is_completed: Boolean, default False, not nullable
   - created_at: DateTime, server_default=func.now(), not nullable
   - updated_at: DateTime, server_default=func.now(),
     onupdate=func.now(), not nullable
   - __tablename__ = "todos"
   - __repr__ for debugging

2. backend/app/schemas/todo.py
   Pydantic v2 schemas:
   - TodoCreate: title (min_length=1, max_length=200, strip whitespace),
     description (optional, max_length=1000)
   - TodoUpdate: all fields optional (PATCH semantics)
   - TodoResponse: all fields, model_config = ConfigDict(from_attributes=True)
   - TodoListResponse: items: list[TodoResponse], total: int

3. backend/app/repositories/todo_repository.py
   TodoRepository class:
   - __init__(self, db: Session)
   - get_by_id(self, todo_id: int) -> Todo | None
   - get_all(self) -> list[Todo]
   - create(self, todo_data: TodoCreate) -> Todo
   - update(self, todo: Todo, update_data: TodoUpdate) -> Todo
   - delete(self, todo: Todo) -> None
   - Full Google docstrings on all methods

4. backend/app/services/todo_service.py
   TodoService class:
   - __init__(self, repository: TodoRepository)
   - get_todo(self, todo_id: int) -> Todo
   - list_todos(self) -> TodoListResponse
   - create_todo(self, data: TodoCreate) -> Todo
   - update_todo(self, todo_id: int, data: TodoUpdate) -> Todo
   - delete_todo(self, todo_id: int) -> None
   - complete_todo(self, todo_id: int) -> Todo  [idempotent]
   - uncomplete_todo(self, todo_id: int) -> Todo  [idempotent]
   - Full Google docstrings on all methods

5. backend/app/routers/todos.py
   APIRouter(prefix="/api/v1/todos", tags=["todos"])
   Endpoints:
   - GET    /             → list todos       → 200 TodoListResponse
   - POST   /             → create todo      → 201 TodoResponse
   - GET    /{todo_id}    → get todo         → 200 TodoResponse
   - PUT    /{todo_id}    → update todo      → 200 TodoResponse
   - DELETE /{todo_id}    → delete todo      → 204
   - PATCH  /{todo_id}/complete   → 200 TodoResponse
   - PATCH  /{todo_id}/uncomplete → 200 TodoResponse
   Map TodoNotFoundError → 404, validation errors → 422

6. Update backend/app/main.py
   Import and include todos router
```

---

### 1.4 — Alembic Initial Migration

Ask Copilot:

```
Ensure backend/alembic/env.py correctly imports the Todo model
from backend/app/models/todo.py so autogenerate detects it.
Show the exact terminal commands to create the virtual environment,
install requirements, generate the migration, and apply it.
```

Then run in terminal:

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
copy .env.example .env
# Edit .env if your SQL Server instance name differs

# Generate migration
alembic revision --autogenerate -m "create_todos_table"

# Review generated file in alembic/versions/ then apply:
alembic upgrade head
```

Verify in SQL Server Management Studio that `todos` and `alembic_version` tables exist.

```bash
git add .
git commit -m "feat(todos): scaffold backend with todo model, repository, service, and router"
git push -u origin feature/basic-todo-api
```

---

### 1.5 — Run and Test Backend (Step 2)

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs` and test each endpoint:

```
Manual test sequence via Swagger UI:

1.  POST /api/v1/todos
    Body: {"title": "Buy groceries", "description": "Milk and eggs"}
    Expected: 201, is_completed=false

2.  POST /api/v1/todos
    Body: {"title": "Read a book"}
    Expected: 201, description=null

3.  GET /api/v1/todos
    Expected: 200, total=2

4.  GET /api/v1/todos/1
    Expected: 200 with first todo

5.  GET /api/v1/todos/999
    Expected: 404 with error message

6.  PUT /api/v1/todos/1
    Body: {"title": "Buy groceries and fruit"}
    Expected: 200 with updated title

7.  PATCH /api/v1/todos/1/complete
    Expected: 200, is_completed=true

8.  PATCH /api/v1/todos/1/complete  (again — idempotent test)
    Expected: 200, is_completed=true (no error)

9.  PATCH /api/v1/todos/1/uncomplete
    Expected: 200, is_completed=false

10. DELETE /api/v1/todos/2
    Expected: 204

11. GET /api/v1/todos/2
    Expected: 404

12. POST /api/v1/todos
    Body: {"title": ""}
    Expected: 422 validation error
```

---

### 1.6 — Prompt: Scaffold React Frontend

```
Role:
You are a Senior React Engineer scaffolding a production-grade
React application with TypeScript and Tailwind CSS.

Task:
Scaffold the React frontend project inside the /frontend folder
and generate the complete Phase 1 Todo UI with API integration.

Audience:
A developer building a minimal but well-structured React frontend
following enterprise patterns.

Context:
- Read frontend/.copilot-instructions.md for all rules
- Read docs/TRD.md for component and folder structure
- Vite + React 18 + TypeScript (strict mode)
- Tailwind CSS for all styling
- Axios for API calls — backend runs on http://localhost:8000
- Phase 1: Single page — show todo list, add todo, complete/delete
- No routing library needed yet
- Frontend .env: VITE_API_URL=http://localhost:8000/api/v1

Constraints:
- Functional components and hooks only
- All API state in custom hooks — components receive clean data
- Minimal but complete UI — not bare HTML, not over-engineered
- TypeScript strict mode — no any types
- Tailwind utility classes only

Output:
Generate these files in sequence:

1. frontend/package.json with scripts and dependencies
   (react, react-dom, axios in deps;
    vite, typescript, tailwindcss, @types/react,
    vitest, @testing-library/react in devDeps)

2. frontend/vite.config.ts — standard config + test config

3. frontend/tsconfig.json — strict mode enabled

4. frontend/tailwind.config.js — content paths set correctly

5. frontend/index.html — minimal, loads /src/main.tsx

6. frontend/src/main.tsx — renders App into root

7. frontend/src/types/todo.ts
   Interfaces: Todo, TodoCreate, TodoUpdate

8. frontend/src/api/client.ts
   Axios instance with baseURL from import.meta.env.VITE_API_URL
   Request/response interceptors for error normalisation

9. frontend/src/api/todosApi.ts
   Functions: fetchTodos, fetchTodo, createTodo, updateTodo,
   deleteTodo, completeTodo, uncompleteTodo
   All typed, all use the shared axios client

10. frontend/src/hooks/useTodos.ts
    Returns: { todos, isLoading, error, createTodo, updateTodo,
               deleteTodo, completeTodo, uncompleteTodo }

11. frontend/src/components/TodoForm.tsx
    Form: title input + description textarea + submit button
    Clears on success, shows error on failure

12. frontend/src/components/TodoItem.tsx
    Shows: checkbox, title (strike if done), description,
    created date, delete button. Clean Tailwind card styling.

13. frontend/src/components/TodoList.tsx
    Shows loading spinner, error message, empty state, or
    list of TodoItem components

14. frontend/src/pages/HomePage.tsx
    Composes: page heading, TodoForm, TodoList
    Uses useTodos hook

15. frontend/src/App.tsx
    Renders HomePage

16. frontend/.env.example
    VITE_API_URL=http://localhost:8000/api/v1
```

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173` — verify todos load, create, complete, delete.

---

### 1.7 — AI Code Review Prompt

```
#security-review

Review all files created or modified in the feature/basic-todo-api
branch compared to main.

Focus on:
1. Any violations of Route → Service → Repository boundaries
2. Missing type hints or docstrings in backend files
3. Any raw SQL or ORM misuse
4. Unhandled exceptions that could crash the server
5. Any credentials or secrets in source files
6. Frontend: any API errors swallowed silently
7. Frontend: any TypeScript any types used

Produce a structured report with BLOCKER, WARNING, SUGGESTION
levels. Fix all BLOCKERs before committing.
```

Fix any BLOCKERs, then:

```bash
cd ..   # repo root
git add .
git commit -m "feat(todos): add full-stack todo feature — backend and frontend"
git push
```

---

### 1.8 — Raise and Merge PR

```bash
gh pr create \
  --title "feat: basic todo application — full stack" \
  --body "## Summary
- FastAPI backend with Route → Service → Repository architecture
- Todo model, Alembic migration, full CRUD endpoints
- React + Tailwind frontend with useTodos hook
- End-to-end verified via Swagger and browser

## Checklist
- [ ] All 7 API endpoints tested via Swagger
- [ ] Frontend creates, completes, deletes todos
- [ ] 404 returned for non-existent todos
- [ ] 422 returned for empty title
- [ ] No secrets in any committed file
- [ ] Copilot security review completed" \
  --base main
```

After review, merge:

```bash
git checkout main && git pull
git branch -d feature/basic-todo-api
```

---

## Phase 2: Unit Tests (Steps 3 & 4)

---

### 2.1 — Create Feature Branch

```bash
git checkout main && git pull
git checkout -b feature/unit-tests-basic-todo
```

---

### 2.2 — Prompt: Generate Backend Tests

```
#test-generation

Role:
You are a Senior Python QA Engineer generating comprehensive tests
for a FastAPI + SQLAlchemy application.

Task:
Generate the complete backend test suite for the Todo resource
covering all three layers: repository, service, and router.

Audience:
The development team who will run and maintain these tests.

Context:
- Read backend/.copilot-instructions.md for testing patterns
- Read all source files before writing any tests:
  backend/app/models/todo.py
  backend/app/schemas/todo.py
  backend/app/repositories/todo_repository.py
  backend/app/services/todo_service.py
  backend/app/routers/todos.py
  backend/app/exceptions.py
- Tests use SQLite in-memory — never SQL Server
- Repository tests: real SQLite session
- Service tests: MagicMock repository
- Router tests: FastAPI TestClient with overridden get_db

Constraints:
- Test every public method and every outcome
- Test names: test_<what>_when_<condition>
- Arrange / Act / Assert structure in every test
- No shared mutable state — each test fully independent
- One-line docstring on every test function

Output — generate in this order:

1. backend/tests/conftest.py
   Fixtures:
   - engine: SQLite in-memory, creates all tables from Base metadata
   - db_session: fresh session per test, rolls back after each test
   - client: TestClient with get_db overridden to use db_session
   - sample_todo: inserts one todo, returns it
   - completed_todo: inserts one completed todo

2. backend/tests/test_todo_repository.py
   - test_create_when_valid_data_returns_todo_with_id
   - test_create_when_called_persists_to_database
   - test_get_by_id_when_exists_returns_correct_todo
   - test_get_by_id_when_not_exists_returns_none
   - test_get_all_when_todos_exist_returns_all
   - test_get_all_when_empty_returns_empty_list
   - test_update_when_valid_data_persists_changes
   - test_update_when_partial_data_only_updates_provided_fields
   - test_delete_when_exists_removes_from_database
   - test_delete_when_called_get_by_id_returns_none_after

3. backend/tests/test_todo_service.py
   Tests using MagicMock repository:
   - test_get_todo_when_exists_returns_todo
   - test_get_todo_when_not_found_raises_todo_not_found_error
   - test_list_todos_returns_todo_list_response
   - test_create_todo_when_valid_calls_repository_create
   - test_create_todo_returns_created_todo
   - test_update_todo_when_exists_calls_repository_update
   - test_update_todo_when_not_found_raises_todo_not_found_error
   - test_delete_todo_when_exists_calls_repository_delete
   - test_delete_todo_when_not_found_raises_todo_not_found_error
   - test_complete_todo_sets_is_completed_true
   - test_complete_todo_when_already_complete_is_idempotent
   - test_uncomplete_todo_sets_is_completed_false
   - test_uncomplete_todo_when_already_incomplete_is_idempotent

4. backend/tests/test_todos_router.py
   Tests using TestClient:
   - test_get_todos_returns_200_with_list
   - test_get_todos_returns_correct_total_count
   - test_get_todo_when_exists_returns_200
   - test_get_todo_when_not_exists_returns_404
   - test_create_todo_with_valid_data_returns_201
   - test_create_todo_response_contains_correct_title
   - test_create_todo_with_empty_title_returns_422
   - test_update_todo_when_exists_returns_200
   - test_update_todo_when_not_exists_returns_404
   - test_delete_todo_when_exists_returns_204
   - test_delete_todo_when_not_exists_returns_404
   - test_complete_todo_returns_200_with_is_completed_true
   - test_uncomplete_todo_returns_200_with_is_completed_false
   - test_complete_todo_on_nonexistent_returns_404
```

---

### 2.3 — Prompt: Generate Frontend Tests

```
#test-generation

Task:
Generate frontend tests for the Phase 1 Todo components and hook.

Context:
- Read frontend/.copilot-instructions.md for testing patterns
- Read all frontend source files before writing tests
- Vitest + React Testing Library
- Mock todosApi module with vi.mock()
- Test behaviour, not implementation

Output:

1. frontend/src/hooks/useTodos.test.ts
   - should return empty todos and isLoading false initially
   - should fetch todos on mount and set data
   - should set isLoading true during fetch
   - should set error when fetch fails
   - should add todo to list when createTodo succeeds
   - should remove todo from list when deleteTodo succeeds
   - should update todo in list when completeTodo succeeds

2. frontend/src/components/TodoForm.test.tsx
   - should render title input and submit button
   - should call createTodo with correct data on submit
   - should clear input after successful submission
   - should show error message when createTodo fails

3. frontend/src/components/TodoItem.test.tsx
   - should render todo title
   - should show strikethrough when todo is completed
   - should call completeTodo when checkbox clicked
   - should call deleteTodo when delete button clicked

4. frontend/src/components/TodoList.test.tsx
   - should show loading indicator when isLoading is true
   - should show error message when error is present
   - should show empty state when todos is empty list
   - should render correct number of TodoItem components
```

---

### 2.4 — Run All Tests (Step 4)

```bash
# Backend
cd backend
pytest -v --tb=short

# With coverage
pytest --cov=app --cov-report=term-missing

# Frontend
cd ../frontend
npm run test
```

If any tests fail, paste the error into Copilot Chat:

```
This test is failing. Read the test file and the source file.
Identify whether the bug is in the test assertion or the source
code. Fix only source code if it is a bug — do not change test
assertions unless the test is logically wrong.

[paste error output here]
```

Once all pass:

```bash
git add .
git commit -m "test(todos): add comprehensive unit and integration tests — all passing"
git push -u origin feature/unit-tests-basic-todo
```

```bash
gh pr create \
  --title "test: add unit and integration tests for todo feature" \
  --body "## Summary
- Repository tests: 10 tests
- Service tests: 13 tests with mocked repository
- Router tests: 13 integration tests with TestClient
- Frontend hook and component tests
- All passing, coverage >85% on backend" \
  --base main
```

```bash
git checkout main && git pull
git branch -d feature/unit-tests-basic-todo
```

---

## Phase 3: Add Category (Steps 5 & 6)

---

### 3.1 — Create Feature Branch

```bash
git checkout main && git pull
git checkout -b feature/add-category
```

---

### 3.2 — Prompt: Generate Category Feature — Full Stack

```
Role:
You are a Senior Python Engineer evolving an existing FastAPI
application by adding a new feature domain.

Task:
Add the Category feature to the Todo application — database model
through API router, plus updating Todo to support categories,
plus updating the React frontend.

Audience:
The development team maintaining this codebase.

Context:
- Read ALL existing files in backend/app/ before making any changes
- Read backend/.copilot-instructions.md strictly
- Read docs/PRD.md Phase 2 requirements
- This is an additive change — do not break any existing functionality
- Category entity: id, name (unique), colour (hex, nullable), created_at
- Todo gets new nullable FK: category_id → categories.id
- Filter todos by category_id query param on GET /api/v1/todos
- Read frontend source files before updating UI

Constraints:
- All existing tests must still pass after these changes
- Alembic handles migration — no manual schema changes
- Strict Route → Service → Repository for category too
- Category deletion must be prevented if todos are assigned (409)
- Google-style docstrings on all new and modified methods

Output — in this exact order:

1. backend/app/models/category.py
   - Category model: id, name (String 100, unique, not null),
     colour (String 7, nullable), created_at (server_default now)
   - Relationship: todos (back_populates="category")

2. Update backend/app/models/todo.py
   - Add: category_id (Integer, ForeignKey categories.id, nullable)
   - Add: relationship to Category (back_populates="todos")

3. backend/app/schemas/category.py
   - CategoryCreate: name (min 1, max 100), colour (optional,
     must match regex ^#[0-9A-Fa-f]{6}$ if provided)
   - CategoryUpdate: both optional
   - CategoryResponse: id, name, colour, created_at,
     from_attributes=True

4. Update backend/app/schemas/todo.py
   - TodoCreate: add category_id (optional int)
   - TodoUpdate: add category_id (optional int)
   - TodoResponse: add category (optional CategoryResponse)

5. backend/app/repositories/category_repository.py
   - CategoryRepository: get_by_id, get_all, create, update,
     delete, get_by_name
   - has_todos(self, category_id: int) -> bool

6. Update backend/app/repositories/todo_repository.py
   - get_all: add optional category_id filter parameter
   - create: handle category_id
   - Queries eager-load category relationship

7. backend/app/services/category_service.py
   - CategoryService: full CRUD
   - delete_category: check has_todos → raise CategoryHasTodosError

8. Update backend/app/services/todo_service.py
   - list_todos: accept optional category_id filter
   - create_todo: validate category exists if provided

9. backend/app/routers/categories.py
   - APIRouter(prefix="/api/v1/categories", tags=["categories"])
   - GET /             → 200 list[CategoryResponse]
   - POST /            → 201 CategoryResponse
   - GET /{id}         → 200 CategoryResponse
   - PUT /{id}         → 200 CategoryResponse
   - DELETE /{id}      → 204 (or 409 if todos assigned)

10. Update backend/app/routers/todos.py
    - GET / — add optional category_id: int query parameter

11. Update backend/app/exceptions.py
    - Add: CategoryNotFoundError, DuplicateCategoryNameError,
      CategoryHasTodosError

12. Update backend/app/main.py
    - Include categories router

13. Update frontend/src/types/todo.ts
    - Add Category interface
    - Update Todo to include optional category

14. frontend/src/api/categoriesApi.ts
    - fetchCategories, createCategory, updateCategory, deleteCategory

15. frontend/src/hooks/useCategories.ts
    - Returns: { categories, isLoading, error, createCategory,
                 updateCategory, deleteCategory }

16. Update frontend/src/hooks/useTodos.ts
    - Add filterByCategory, accept selectedCategoryId

17. frontend/src/components/CategoryBadge.tsx
    - Coloured pill showing category name

18. frontend/src/components/CategoryFilter.tsx
    - "All" pill + one per category, highlights selected

19. frontend/src/components/CategoryForm.tsx
    - name input + colour picker input

20. Update frontend/src/components/TodoForm.tsx
    - Add category selector dropdown

21. Update frontend/src/components/TodoItem.tsx
    - Show CategoryBadge if todo has category

22. Update frontend/src/pages/HomePage.tsx
    - Add CategoryFilter, CategoryForm
    - Wire up selectedCategoryId state
```

---

### 3.3 — Alembic Migration for Category

```bash
cd backend

# Verify env.py imports Category model, then:
alembic revision --autogenerate -m "add_categories_table_and_todo_fk"

# Review generated migration file — should:
# - Create categories table
# - Add category_id FK column to todos

alembic upgrade head
```

Verify in SSMS that both changes are applied.

```bash
git add .
git commit -m "feat(categories): add category model, alembic migration applied"
git push -u origin feature/add-category
```

---

### 3.4 — Prompt: Update Tests for Category (Step 6)

```
#test-generation

Role:
You are a Senior QA Engineer extending an existing test suite
to cover a newly added feature.

Task:
Generate tests for the Category feature and update existing
Todo tests to cover the new category-related behaviour.

Audience:
The development team maintaining these tests.

Context:
- Read ALL existing test files before generating new tests
- Read all new Category source files
- Read updated todo source files
- Follow same patterns as existing tests

Constraints:
- Extend conftest.py with category fixtures
- New test files mirror source file names
- Must not break any currently passing tests
- Category deletion with assigned todos must test 409 response

Output:

1. Update backend/tests/conftest.py
   - Add fixture: sample_category
   - Add fixture: todo_with_category

2. backend/tests/test_category_repository.py
   - test_create_when_valid_returns_category
   - test_create_persists_to_database
   - test_get_by_id_when_exists_returns_category
   - test_get_by_id_when_not_exists_returns_none
   - test_get_all_returns_all_categories
   - test_get_by_name_when_exists_returns_category
   - test_update_persists_changes
   - test_delete_removes_from_database
   - test_has_todos_when_assigned_returns_true
   - test_has_todos_when_not_assigned_returns_false

3. backend/tests/test_category_service.py
   - test_create_category_when_name_unique_returns_category
   - test_create_category_when_name_duplicate_raises_error
   - test_get_category_when_not_found_raises_category_not_found_error
   - test_update_category_when_not_found_raises_error
   - test_delete_category_when_no_todos_calls_repository_delete
   - test_delete_category_when_todos_assigned_raises_category_has_todos_error

4. backend/tests/test_categories_router.py
   - test_get_categories_returns_200_with_list
   - test_create_category_returns_201
   - test_create_category_with_duplicate_name_returns_409
   - test_get_category_returns_200
   - test_get_category_not_found_returns_404
   - test_update_category_returns_200
   - test_delete_category_when_no_todos_returns_204
   - test_delete_category_when_todos_assigned_returns_409

5. Update backend/tests/test_todos_router.py
   - test_create_todo_with_valid_category_id_returns_201
   - test_create_todo_with_invalid_category_id_returns_404
   - test_get_todos_with_category_filter_returns_filtered_results
   - test_todo_response_includes_category_object_when_assigned

6. Update frontend tests
   - CategoryForm, CategoryFilter, CategoryBadge component tests
   - Update TodoItem test for category badge
   - useCategories hook tests
```

Run tests:

```bash
cd backend && pytest -v --tb=short
cd ../frontend && npm run test
```

Once all pass:

```bash
git add .
git commit -m "test(categories): add category tests, update todo tests — all passing"
git push
```

---

### 3.5 — End-to-End Verification

```
✓ Create category "Work" with colour #3B82F6
✓ Create category "Personal" with colour #10B981
✓ Create todo "Send report" → assign to Work
✓ CategoryBadge appears on todo item
✓ CategoryFilter pill shows and filters correctly
✓ Attempt delete category with todos → 409 error shown in UI
✓ Delete todos first → then delete empty category → 204
```

```bash
gh pr create \
  --title "feat: add category feature — full stack with tests" \
  --body "## Summary
- Category model, repository, service, router (full CRUD)
- Todo updated with nullable category FK
- Alembic migration: add_categories_table_and_todo_fk
- Category filter on GET /api/v1/todos
- React UI: CategoryFilter, CategoryForm, CategoryBadge
- All existing tests pass + new category tests added

## Migration applied
alembic upgrade head — DB schema updated

## Test results
pytest: X passed, 0 failed
npm test: X passed, 0 failed" \
  --base main
```

```bash
git checkout main && git pull
git branch -d feature/add-category
```

---

## Phase 4: Edge Cases & Hardening (Steps 7, 8 & 9)

---

### 4.1 — Create Feature Branch

```bash
git checkout main && git pull
git checkout -b feature/edge-cases
```

---

### 4.2 — Prompt: Generate Edge Case Tests (Step 7 — designed to fail)

```
Role:
You are a Senior QA Engineer specialising in boundary conditions,
negative testing, and adversarial input scenarios.

Task:
Generate edge case tests deliberately designed to expose gaps in
the current implementation. These tests WILL FAIL initially.

Audience:
The development team who will use these failures to find and fix
weaknesses in the application.

Context:
- Read ALL current source files and ALL current test files
- Focus on: boundary values, invalid inputs, whitespace, null/empty
  strings, referential integrity, max length violations, special
  characters, malformed data, ordering, idempotency
- Do not modify any existing passing tests

Constraints:
- Mark every new test with comment:
  # EDGE CASE — may fail until source code is fixed
- Do not modify source code in this step
- Be thorough — think like someone trying to break the API

Output:
Add these tests to existing test files:

In backend/tests/test_todos_router.py:
- test_create_todo_with_whitespace_only_title_returns_422
- test_create_todo_with_title_at_max_length_returns_201
  (title exactly 200 chars — should succeed)
- test_create_todo_with_title_exceeding_max_length_returns_422
  (title 201 chars)
- test_create_todo_with_description_exceeding_max_length_returns_422
  (description 1001 chars)
- test_update_todo_with_whitespace_only_title_returns_422
- test_update_todo_with_empty_string_title_returns_422
- test_delete_todo_when_already_deleted_second_call_returns_404
- test_get_todos_default_order_is_newest_first
- test_complete_todo_is_idempotent_returns_200_not_error
- test_create_todo_with_null_title_returns_422
- test_get_todos_with_nonexistent_category_id_returns_empty_list

In backend/tests/test_categories_router.py:
- test_create_category_with_invalid_colour_hex_returns_422
  (colour="red" — not hex format)
- test_create_category_with_whitespace_only_name_returns_422
- test_create_category_name_is_trimmed_before_storage
  (name="  Work  " stored as "Work")
- test_update_category_to_existing_name_returns_409
- test_delete_category_with_todos_returns_409_with_message
- test_create_category_with_name_at_max_length_returns_201
  (100 chars exactly)
- test_create_category_with_name_exceeding_max_length_returns_422
  (101 chars)

In backend/tests/test_todo_service.py:
- test_create_todo_with_whitespace_title_raises_validation_error
- test_list_todos_ordered_by_created_at_descending
- test_create_todo_with_nonexistent_category_id_raises_category_not_found_error
```

Run and document failures:

```bash
cd backend
pytest -v --tb=short 2>&1 | tee edge_case_failures.txt
```

---

### 4.3 — Prompt: Fix Source Code to Pass Edge Cases (Step 8)

```
Role:
You are a Senior Python Engineer fixing implementation gaps
revealed by failing edge case tests.

Task:
Fix all failing edge case tests by updating source code only.
Do not modify any test files.

Audience:
The development team who will verify all tests pass after fixes.

Context:
- Read edge_case_failures.txt (or paste failing test output)
- Read these source files before making any changes:
  backend/app/schemas/todo.py
  backend/app/schemas/category.py
  backend/app/services/todo_service.py
  backend/app/services/category_service.py
  backend/app/repositories/todo_repository.py
  backend/app/repositories/category_repository.py
- The tests define correct behaviour — make code match them
- All currently passing tests must continue to pass

Constraints:
- Do not modify any test file
- Fix root cause, not just the symptom
- Add a code comment explaining each fix
- Every fix must be the minimal change needed

Output — fix these specific issues:

1. backend/app/schemas/todo.py
   - Add @field_validator on title: strip whitespace, then
     check min_length after stripping
   - Enforce max_length=200 on title
   - Enforce max_length=1000 on description
   - TodoUpdate: same validators on title if provided

2. backend/app/schemas/category.py
   - Name: strip whitespace + validate min_length after strip
   - Name: max_length=100
   - Colour: regex validator ^#[0-9A-Fa-f]{6}$ (only when provided)

3. backend/app/repositories/todo_repository.py
   - get_all: add order_by(Todo.created_at.desc()) as default

4. backend/app/services/category_service.py
   - update_category: check if new name belongs to a different
     category — raise DuplicateCategoryNameError if so

5. backend/app/services/todo_service.py
   - list_todos with nonexistent category_id: return empty
     TodoListResponse (not an error — valid filter with no results)

6. Verify complete_todo and uncomplete_todo are truly idempotent
   (no exception when already in desired state)

After fixes:
pytest -v --tb=short
```

---

### 4.4 — Run All Tests (Step 9)

```bash
cd backend
pytest -v --tb=short

# Once all pass:
pytest --cov=app --cov-report=term-missing
```

Target: **0 failures**, coverage **≥ 85%**.

---

### 4.5 — Security Review

```
#security-review

Perform a full security review of all files changed in the
feature/edge-cases branch compared to main.

Also review the entire backend/app/ folder for any issues
introduced across all three feature branches.

Pay special attention to:
1. Colour field hex validation — is the regex correct?
2. Category 409 response — does it expose internal DB details?
3. Error messages across all endpoints — any implementation leakage?
4. Are validators applied consistently to both Create and Update schemas?

Produce the full structured report. Flag any BLOCKER that must
be resolved before merging to main.
```

Fix any BLOCKERs, then:

```bash
git add .
git commit -m "fix(validation): resolve edge case failures — input validation and ordering"
git commit -m "test(edge-cases): all edge case tests now passing"
git push -u origin feature/edge-cases
```

```bash
gh pr create \
  --title "fix: edge case hardening — validation, ordering, referential integrity" \
  --body "## Summary
- Added 19 edge case tests covering boundary conditions
- Fixed: whitespace validation on title and category name
- Fixed: max length enforcement on all string fields
- Fixed: hex colour format validation
- Fixed: default ordering on GET /todos (newest first)
- Fixed: update category duplicate name check (409)
- Fixed: list todos with nonexistent category → empty (not 404)
- Security review completed — all BLOCKERs resolved

## Test results
pytest: X passed, 0 failed
Coverage: XX%" \
  --base main
```

```bash
git checkout main && git pull
git branch -d feature/edge-cases
```

---

## Phase 5: Final Polish & Wrap-up (Step 10)

---

### 5.1 — Create Feature Branch

```bash
git checkout main && git pull
git checkout -b feature/final-polish
```

---

### 5.2 — Prompt: Generate README

```
Task:
Generate a comprehensive README.md for the todo-app repository.

Context:
- Read docs/PRD.md and docs/TRD.md
- Read backend/requirements.txt and frontend/package.json
- Monorepo: /backend (FastAPI) and /frontend (React + Tailwind)
- SQL Server Express, Windows Auth, local machine only
- Include actual commands that work on Windows

Output:
Create README.md at repository root with:
1. Project overview (2-3 sentences)
2. Tech stack table
3. Prerequisites with version numbers
4. Repository structure (folder tree)
5. Backend setup:
   - CREATE DATABASE TodoDB in SQL Server
   - Create and activate venv
   - pip install -r requirements.txt
   - Copy .env.example to .env
   - alembic upgrade head
   - uvicorn app.main:app --reload
6. Frontend setup:
   - npm install
   - Copy .env.example to .env
   - npm run dev
7. Running tests:
   - Backend: pytest -v
   - Frontend: npm run test
8. API documentation link: http://localhost:8000/docs
9. Development workflow:
   - Branch naming
   - How to invoke #test-generation skill
   - How to invoke #security-review skill
   - PR checklist
10. Project phases overview
```

---

### 5.3 — Final Comprehensive Code Review

```
#security-review

Perform a final comprehensive review of the entire codebase
across both /backend and /frontend.

This is the final quality gate before tagging v1.0.0.

Check:
1. All architecture rules followed in every file
2. No missing docstrings on any public function or class
3. All exception paths handled — no unhandled exceptions
4. All API inputs validated via Pydantic
5. Frontend: no console.log left in code
6. Frontend: all loading and error states handled in UI
7. Test coverage adequate across all modules
8. README setup instructions are accurate
9. No .env file committed anywhere in repo
10. All TODO comments resolved or documented

Produce final PASS / NEEDS WORK verdict with full findings.
```

---

### 5.4 — Run the Final Application (Step 10)

**Terminal 1 — Backend:**

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**

```bash
cd frontend
npm run dev
```

**Final end-to-end verification checklist:**

```
Backend health:
  ✓ GET http://localhost:8000/health → {"status": "healthy"}
  ✓ GET http://localhost:8000/docs → Swagger UI loads

Category management:
  ✓ Create category "Work" with colour #3B82F6
  ✓ Create category "Personal" with colour #10B981
  ✓ Create category "Shopping" with no colour
  ✓ Rename "Shopping" → "Errands"
  ✓ Try invalid colour "red" → 422 error shown

Todo management:
  ✓ Create todo "Send project report" → assign to Work
  ✓ Create todo "Buy milk" → assign to Errands
  ✓ Create todo "Read novel" → assign to Personal
  ✓ Create todo "Morning run" → no category
  ✓ All 4 todos visible (newest first)

Filtering:
  ✓ Click "Work" → only "Send project report" shows
  ✓ Click "All" → all todos show

Todo operations:
  ✓ Complete "Buy milk" → strikethrough appears
  ✓ Uncomplete "Buy milk" → strikethrough removed
  ✓ Edit "Send project report" title
  ✓ Delete "Morning run"

Edge cases in UI:
  ✓ Submit empty title → form prevents it
  ✓ Delete "Work" category (has todos) → 409 error shown
  ✓ Delete all Work todos → delete "Work" succeeds

Final test run:
  ✓ cd backend && pytest --cov=app --cov-report=term-missing
  ✓ cd frontend && npm run test
  ✓ All tests pass
```

---

### 5.5 — Final Commit, PR, and Tag

```bash
git add .
git commit -m "docs(readme): add comprehensive README with setup instructions"
git commit -m "chore(final): final polish — code review findings resolved"
git push -u origin feature/final-polish
```

```bash
gh pr create \
  --title "chore: final polish and README — ready for v1.0.0" \
  --body "## Summary
- Comprehensive README with full setup instructions
- Final security review completed — all issues resolved
- End-to-end verified across all features

## Final test results
pytest: X passed, 0 failed, coverage XX%
npm test: X passed, 0 failed

## Checklist
- [x] All tests passing
- [x] No console.log in frontend
- [x] No .env committed
- [x] README accurate and complete
- [x] All docstrings present
- [x] Security review: PASS" \
  --base main
```

Merge and tag:

```bash
git checkout main && git pull
git branch -d feature/final-polish

# Tag the release
git tag -a v1.0.0 -m "Release v1.0.0 — Todo app with categories, full test suite"
git push origin v1.0.0
```

---

## Quick Reference — All Prompts and Commands

| Phase | Step | Branch | Action |
|---|---|---|---|
| 0 | PRD | main | Prompt 0.3 → docs/PRD.md |
| 0 | TRD | main | Prompt 0.4 → docs/TRD.md |
| 0 | Shared instructions | main | Prompt 0.5 → .github/copilot-instructions.md |
| 0 | Backend instructions | main | Prompt 0.6 → backend/.copilot-instructions.md |
| 0 | Frontend instructions | main | Prompt 0.7 → frontend/.copilot-instructions.md |
| 0 | Test generation skill | main | Prompt 0.8 → .github/prompts/test-generation.prompt.md |
| 0 | Security review skill | main | Prompt 0.9 → .github/prompts/security-review.prompt.md |
| 1 | Backend scaffold | feature/basic-todo-api | Prompt 1.2 |
| 1 | Todo feature — all layers | feature/basic-todo-api | Prompt 1.3 |
| 1 | Initial migration | feature/basic-todo-api | alembic revision + upgrade |
| 1 | Manual backend test | feature/basic-todo-api | Swagger UI at /docs |
| 1 | Frontend scaffold | feature/basic-todo-api | Prompt 1.6 |
| 1 | Code review | feature/basic-todo-api | #security-review |
| 2 | Backend tests | feature/unit-tests-basic-todo | #test-generation Prompt 2.2 |
| 2 | Frontend tests | feature/unit-tests-basic-todo | #test-generation Prompt 2.3 |
| 2 | Run tests | feature/unit-tests-basic-todo | pytest + npm test |
| 3 | Category feature | feature/add-category | Prompt 3.2 |
| 3 | Category migration | feature/add-category | alembic revision + upgrade |
| 3 | Category tests | feature/add-category | #test-generation Prompt 3.4 |
| 4 | Edge case tests | feature/edge-cases | Prompt 4.2 (expect failures) |
| 4 | Fix source code | feature/edge-cases | Prompt 4.3 |
| 4 | Final security review | feature/edge-cases | #security-review |
| 5 | README | feature/final-polish | Prompt 5.2 |
| 5 | Final review | feature/final-polish | #security-review |
| 5 | Tag release | main | git tag v1.0.0 |

---

## Data Model Reference

### Phase 1 — todos table

| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, autoincrement |
| title | String(200) | not null |
| description | String(1000) | nullable |
| is_completed | Boolean | default false, not null |
| created_at | DateTime | server_default now, not null |
| updated_at | DateTime | server_default now, onupdate now |

### Phase 2 — categories table

| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, autoincrement |
| name | String(100) | not null, unique |
| colour | String(7) | nullable, hex format |
| created_at | DateTime | server_default now |

### Phase 2 — todos table additions

| Column | Type | Constraints |
|---|---|---|
| category_id | Integer | nullable, FK → categories.id |

---

## API Endpoints Reference

### Phase 1 — Todos

| Method | Path | Description | Status codes |
|---|---|---|---|
| GET | /api/v1/todos | List all todos (newest first) | 200 |
| POST | /api/v1/todos | Create todo | 201, 422 |
| GET | /api/v1/todos/{id} | Get single todo | 200, 404 |
| PUT | /api/v1/todos/{id} | Update todo | 200, 404, 422 |
| DELETE | /api/v1/todos/{id} | Delete todo | 204, 404 |
| PATCH | /api/v1/todos/{id}/complete | Mark complete | 200, 404 |
| PATCH | /api/v1/todos/{id}/uncomplete | Mark incomplete | 200, 404 |

### Phase 2 additions

| Method | Path | Description | Status codes |
|---|---|---|---|
| GET | /api/v1/todos?category_id={id} | Filter by category | 200 |
| GET | /api/v1/categories | List all categories | 200 |
| POST | /api/v1/categories | Create category | 201, 422 |
| GET | /api/v1/categories/{id} | Get category | 200, 404 |
| PUT | /api/v1/categories/{id} | Update category | 200, 404, 409, 422 |
| DELETE | /api/v1/categories/{id} | Delete category | 204, 404, 409 |

---

## Commit Message Reference

```
Format: <type>(<scope>): <description>

Types:
  feat     — new feature
  fix      — bug fix
  test     — adding or fixing tests
  refactor — code change without feature or bug
  docs     — documentation only
  chore    — tooling, config, dependencies

Examples:
  feat(todos): add create todo endpoint
  fix(validation): reject whitespace-only title
  test(categories): add repository unit tests
  docs(readme): add backend setup instructions
  chore(deps): pin sqlalchemy to 2.0.30
  refactor(service): extract category validation to helper
```

---

## Invoking Custom Skills

```bash
# In Copilot Chat Agent mode:

# Generate tests for the file currently open:
#test-generation
Generate tests for backend/app/services/category_service.py

# Run security review on current branch:
#security-review
Review all changed files in feature/add-category vs main
```

---

*Generated: March 2026*
*Stack: Python 3.11 · FastAPI · SQLAlchemy 2.x · Alembic · React 18 · Vite · TypeScript · Tailwind CSS · SQL Server Express*
*Tools: GitHub Copilot Individual · VS Code Agent Mode · GitHub CLI*
