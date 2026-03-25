# Technical Requirements Document (TRD)
## Todo Management Application — Phase 1

**Version:** 1.0
**Date:** 2026-03-25
**Phase:** 1 — Core Todo Management (no categories)
**Status:** Draft

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [Folder Structure](#2-folder-structure)
3. [Backend Specifications](#3-backend-specifications)
   - 3.1 [FastAPI Application Setup](#31-fastapi-application-setup)
   - 3.2 [Database Setup — SQLAlchemy Async](#32-database-setup--sqlalchemy-async)
   - 3.3 [Alembic Configuration](#33-alembic-configuration)
   - 3.4 [Models](#34-models)
   - 3.5 [Schemas (Pydantic v2)](#35-schemas-pydantic-v2)
   - 3.6 [Repository Layer](#36-repository-layer)
   - 3.7 [Service Layer](#37-service-layer)
   - 3.8 [Router — API Endpoints](#38-router--api-endpoints)
   - 3.9 [Exception Handling](#39-exception-handling)
   - 3.10 [Configuration](#310-configuration)
4. [Frontend Specifications](#4-frontend-specifications)
5. [Database Design](#5-database-design)
6. [Testing Strategy](#6-testing-strategy)
7. [Development Workflow](#7-development-workflow)
8. [Instruction File Strategy](#8-instruction-file-strategy)

---

## 1. System Architecture

### 1.1 Overview

The application follows a clean, layered architecture for the backend with a decoupled single-page application (SPA) frontend. There is no authentication in Phase 1; the system is single-user.

```
Client (React SPA)
        |
        | HTTP/JSON (Axios)
        v
+-------------------------+
|   FastAPI Application   |
|   (async, ASGI/Uvicorn) |
+-------------------------+
        |
   [Router Layer]          — HTTP routing, request/response validation, HTTP status codes
        |
   [Service Layer]         — Business logic, orchestration, exception translation
        |
   [Repository Layer]      — Data access only, no business logic
        |
   [SQLAlchemy Async ORM]
        |
   [SQL Server Express]    — Persistent storage
+-------------------------+
```

### 1.2 Layered Responsibilities

| Layer | Responsibility | Knows About |
|---|---|---|
| Router | Parse HTTP requests, validate via Pydantic schemas, return HTTP responses | Schemas, Service |
| Service | Business rules, validation logic, raising domain exceptions | Repository, Schemas, Exceptions |
| Repository | CRUD database operations, query construction | Models, AsyncSession |
| Model | SQLAlchemy ORM table definitions | Database |
| Schema | Pydantic v2 request/response contracts | Nothing else |

### 1.3 Async Strategy

- FastAPI runs on Uvicorn (ASGI).
- All database I/O uses `asyncio` via SQLAlchemy 2.x `AsyncSession` and `aioodbc` as the async ODBC driver for SQL Server.
- All route handler functions, service methods, and repository methods are `async def`.
- The `get_db` dependency yields an `AsyncSession` per request and is managed via `async with`.

### 1.4 Technology Stack Summary

| Concern | Technology |
|---|---|
| Frontend | React 18, Vite, TypeScript, Axios |
| Backend Framework | Python 3.11+, FastAPI |
| ORM | SQLAlchemy 2.x (async) |
| DB Driver | aioodbc (async ODBC for SQL Server) |
| Database | SQL Server Express (local) |
| Migrations | Alembic |
| Config | pydantic-settings |
| Testing | pytest, pytest-asyncio, httpx (AsyncClient) |
| Package Manager (BE) | pip / venv |
| Package Manager (FE) | npm |

---

## 2. Folder Structure

The project is a monorepo with a `backend` and `frontend` directory at the root.

```
TodoApplication/
│
├── docs/
│   └── TRD.md                          # This document
│
├── .github/
│   └── copilot-instructions/
│       ├── backend.instructions.md     # Copilot instructions for backend code
│       ├── frontend.instructions.md    # Copilot instructions for frontend code
│       └── testing.instructions.md    # Copilot instructions for test code
│
├── backend/
│   ├── alembic/
│   │   ├── versions/                   # Auto-generated migration scripts
│   │   ├── env.py                      # Alembic env — imports models, uses async engine
│   │   └── script.py.mako              # Migration script template
│   ├── alembic.ini                     # Alembic configuration file
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app factory, lifespan, CORS, router inclusion
│   │   │
│   │   ├── config.py                   # pydantic-settings Settings class
│   │   │
│   │   ├── database.py                 # Async engine, AsyncSessionLocal, get_db dependency
│   │   │
│   │   ├── exceptions.py               # AppException, TodoNotFoundError, ValidationError
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── todo.py                 # Todo SQLAlchemy model
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── todo.py                 # TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
│   │   │
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   └── todo_repository.py      # TodoRepository class
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── todo_service.py         # TodoService class
│   │   │
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── todo_router.py          # /api/v1/todos endpoints
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                 # pytest fixtures: async engine, test DB session, AsyncClient
│   │   ├── test_todo_router.py         # Integration tests (router -> service -> real test DB)
│   │   ├── test_todo_service.py        # Unit tests (service with mock repository)
│   │   └── test_todo_repository.py     # Integration tests (repository against test DB)
│   │
│   ├── requirements.txt                # Production dependencies
│   └── requirements-dev.txt           # Dev/test dependencies
│
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.tsx                    # React DOM root render
│   │   ├── App.tsx                     # Root component, routing setup
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── api/
│   │   │   ├── axiosInstance.ts        # Configured Axios instance (baseURL, interceptors)
│   │   │   └── todoApi.ts              # All todo API call functions
│   │   │
│   │   ├── types/
│   │   │   └── todo.ts                 # TypeScript interfaces: Todo, TodoCreate, TodoUpdate
│   │   │
│   │   ├── hooks/
│   │   │   └── useTodos.ts             # Custom React hook for todo state and API calls
│   │   │
│   │   ├── components/
│   │   │   ├── TodoList.tsx            # Renders list of TodoItem components
│   │   │   ├── TodoItem.tsx            # Single todo row with actions
│   │   │   ├── TodoForm.tsx            # Create / edit todo form
│   │   │   └── ErrorMessage.tsx        # Reusable error display component
│   │   │
│   │   └── pages/
│   │       └── TodoPage.tsx            # Main page composing all todo components
│   │
│   ├── index.html
│   ├── vite.config.ts                  # Vite config with proxy to backend
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── package.json
│
└── .gitignore
```

---

## 3. Backend Specifications

### 3.1 FastAPI Application Setup

**File:** `backend/app/main.py`

#### Lifespan

Use FastAPI's `lifespan` context manager (replacing deprecated `on_event`) to manage startup and shutdown logic. On startup, the application verifies the database connection. On shutdown, the async engine is disposed.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: optionally verify DB connectivity
    yield
    # shutdown: dispose engine
    await engine.dispose()

app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)
```

#### CORS

CORS is configured to allow the Vite dev server origin during development. The allowed origins are driven by the `Settings` config object so they can be changed per environment without code changes.

- `allow_origins`: list from settings (e.g., `["http://localhost:5173"]`)
- `allow_credentials`: `True`
- `allow_methods`: `["*"]`
- `allow_headers`: `["*"]`

Use `fastapi.middleware.cors.CORSMiddleware`.

#### Router Inclusion

All todo endpoints are registered under the `/api/v1` prefix:

```python
from app.routers.todo_router import router as todo_router
app.include_router(todo_router, prefix="/api/v1")
```

#### Global Exception Handlers

Register handlers for `AppException` and unhandled `Exception` to return consistent JSON error responses:

```python
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
```

---

### 3.2 Database Setup — SQLAlchemy Async

**File:** `backend/app/database.py`

#### Engine

Use `sqlalchemy.ext.asyncio.create_async_engine` with the `aioodbc` dialect. The connection string format for SQL Server via aioodbc is:

```
mssql+aioodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=TodoDB;Trusted_Connection=yes;
```

Engine settings:
- `echo`: driven by `settings.DEBUG`
- `pool_pre_ping`: `True` — validates connections before use
- `pool_size`: `5`
- `max_overflow`: `10`

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

#### `get_db` Dependency

Yields one `AsyncSession` per request. The session is committed on success and rolled back on exception, then closed.

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

#### Declarative Base

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

All models import and inherit from this `Base`. Alembic's `env.py` imports `Base.metadata` for autogenerate.

---

### 3.3 Alembic Configuration

**File:** `backend/alembic.ini`

- `script_location = alembic`
- `sqlalchemy.url` is left intentionally blank or set to a placeholder; the actual URL is injected at runtime from `settings.DATABASE_URL` inside `alembic/env.py`.

**File:** `backend/alembic/env.py`

Key requirements:
- Import `Base` from `app.database` and all models so metadata is populated.
- Use the async-compatible Alembic runner pattern (`run_async_migrations`) with `AsyncEngine` and `connectable.connect()` using `run_sync`.
- Set `target_metadata = Base.metadata` for autogenerate support.

```python
from app.database import engine, Base
from app.models import todo  # noqa: F401 — ensure model is registered

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine
    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    asyncio.run(run_async_migrations())
```

**Common Alembic commands:**

```bash
# Generate a new migration after model changes
alembic revision --autogenerate -m "create todos table"

# Apply all pending migrations
alembic upgrade head

# Downgrade one step
alembic downgrade -1
```

---

### 3.4 Models

**File:** `backend/app/models/todo.py`

#### Todo Model

| Column | SQLAlchemy Type | Constraints | Notes |
|---|---|---|---|
| `id` | `Integer` | Primary key, autoincrement, not null | Surrogate key |
| `title` | `String(200)` | Not null | Max 200 characters |
| `description` | `String(1000)` | Nullable | Optional, max 1000 characters |
| `is_completed` | `Boolean` | Not null, default `False`, server_default `'0'` | Completion flag |
| `created_at` | `DateTime` | Not null, default `func.now()`, server_default `func.now()` | Set on insert |
| `updated_at` | `DateTime` | Not null, default `func.now()`, onupdate `func.now()` | Set on insert and update |

```python
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
```

Use SQLAlchemy 2.x `Mapped` and `mapped_column` syntax throughout.

---

### 3.5 Schemas (Pydantic v2)

**File:** `backend/app/schemas/todo.py`

All schemas use Pydantic v2. Use `model_config = ConfigDict(from_attributes=True)` on response schemas to allow ORM model instantiation.

#### `TodoCreate`

Used as the request body for creating a todo.

| Field | Type | Validation |
|---|---|---|
| `title` | `str` | Required, `min_length=1`, `max_length=200` |
| `description` | `str \| None` | Optional, `max_length=1000`, default `None` |

#### `TodoUpdate`

Used as the request body for partial updates. All fields are optional so a PATCH-style update is supported even though the endpoint uses PUT.

| Field | Type | Validation |
|---|---|---|
| `title` | `str \| None` | Optional, `min_length=1`, `max_length=200`, default `None` |
| `description` | `str \| None` | Optional, `max_length=1000`, default `None` |
| `is_completed` | `bool \| None` | Optional, default `None` |

#### `TodoResponse`

Returned for single todo operations. Maps directly from the ORM model.

| Field | Type |
|---|---|
| `id` | `int` |
| `title` | `str` |
| `description` | `str \| None` |
| `is_completed` | `bool` |
| `created_at` | `datetime` |
| `updated_at` | `datetime` |

```python
model_config = ConfigDict(from_attributes=True)
```

#### `TodoListResponse`

Wraps a list of todos with a count for convenience.

| Field | Type |
|---|---|
| `todos` | `list[TodoResponse]` |
| `count` | `int` |

---

### 3.6 Repository Layer

**File:** `backend/app/repositories/todo_repository.py`

The repository is a plain class that receives an `AsyncSession` in its constructor. It contains no business logic — only query construction and execution.

#### `TodoRepository`

```python
class TodoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
```

#### Methods

**`get_by_id(todo_id: int) -> Todo | None`**
- Executes `SELECT * FROM todos WHERE id = :todo_id`.
- Returns the `Todo` ORM instance or `None` if not found.
- Use `session.get(Todo, todo_id)` for primary key lookup.

**`get_all() -> list[Todo]`**
- Executes `SELECT * FROM todos ORDER BY created_at DESC`.
- Returns all `Todo` rows as a list.
- Use `select(Todo).order_by(Todo.created_at.desc())` with `scalars().all()`.

**`create(title: str, description: str | None) -> Todo`**
- Instantiates a new `Todo` ORM object, adds it to the session, flushes (to get the generated `id`), and refreshes the instance.
- Returns the created `Todo`.

**`update(todo: Todo, title: str | None, description: str | None, is_completed: bool | None) -> Todo`**
- Applies only the non-`None` fields to the existing `Todo` instance.
- Flushes and refreshes the instance.
- Returns the updated `Todo`.

**`delete(todo: Todo) -> None`**
- Calls `session.delete(todo)` and flushes.
- Returns nothing.

Note: The `get_db` dependency in `database.py` handles the final `commit()`. The repository only `flush()`es to make changes visible within the session without committing, which is the correct pattern for unit-of-work consistency.

---

### 3.7 Service Layer

**File:** `backend/app/services/todo_service.py`

The service layer holds all business logic and is the only layer that raises domain exceptions. It receives a `TodoRepository` instance in its constructor.

#### `TodoService`

```python
class TodoService:
    def __init__(self, repository: TodoRepository) -> None:
        self.repository = repository
```

#### Methods

**`get_todo(todo_id: int) -> Todo`**
- Calls `repository.get_by_id(todo_id)`.
- If result is `None`, raises `TodoNotFoundError(todo_id)`.
- Returns the `Todo`.

**`list_todos() -> list[Todo]`**
- Calls `repository.get_all()`.
- Returns the list (empty list is valid, not an error).

**`create_todo(data: TodoCreate) -> Todo`**
- Validates that `data.title` is not blank after stripping whitespace; raises `ValidationError` if it is.
- Calls `repository.create(title=data.title.strip(), description=data.description)`.
- Returns the created `Todo`.

**`update_todo(todo_id: int, data: TodoUpdate) -> Todo`**
- Calls `get_todo(todo_id)` (raises `TodoNotFoundError` if missing).
- If `data.title` is provided, validates it is not blank after strip; raises `ValidationError` if it is.
- Calls `repository.update(todo, ...)` with stripped title if provided.
- Returns the updated `Todo`.

**`delete_todo(todo_id: int) -> None`**
- Calls `get_todo(todo_id)` (raises `TodoNotFoundError` if missing).
- Calls `repository.delete(todo)`.

**`complete_todo(todo_id: int) -> Todo`**
- Calls `get_todo(todo_id)` (raises `TodoNotFoundError` if missing).
- Calls `repository.update(todo, is_completed=True)`.
- Returns the updated `Todo`.

**`uncomplete_todo(todo_id: int) -> Todo`**
- Calls `get_todo(todo_id)` (raises `TodoNotFoundError` if missing).
- Calls `repository.update(todo, is_completed=False)`.
- Returns the updated `Todo`.

---

### 3.8 Router — API Endpoints

**File:** `backend/app/routers/todo_router.py`

All endpoints are under the prefix `/api/v1/todos` (prefix set at inclusion time in `main.py`; the router itself uses `APIRouter(tags=["todos"])`).

The router uses FastAPI's `Depends` to inject both the `AsyncSession` (via `get_db`) and the `TodoService` (via a `get_todo_service` dependency factory that creates the repository and service).

```python
async def get_todo_service(db: AsyncSession = Depends(get_db)) -> TodoService:
    repository = TodoRepository(db)
    return TodoService(repository)
```

#### Endpoint Summary

| # | Method | Path | Description | Request Body | Success Response |
|---|---|---|---|---|---|
| 1 | `GET` | `/api/v1/todos` | List all todos | — | `200 TodoListResponse` |
| 2 | `POST` | `/api/v1/todos` | Create a new todo | `TodoCreate` | `201 TodoResponse` |
| 3 | `GET` | `/api/v1/todos/{todo_id}` | Get a single todo | — | `200 TodoResponse` |
| 4 | `PUT` | `/api/v1/todos/{todo_id}` | Update a todo | `TodoUpdate` | `200 TodoResponse` |
| 5 | `DELETE` | `/api/v1/todos/{todo_id}` | Delete a todo | — | `204 No Content` |
| 6 | `PATCH` | `/api/v1/todos/{todo_id}/complete` | Mark todo as complete | — | `200 TodoResponse` |
| 7 | `PATCH` | `/api/v1/todos/{todo_id}/uncomplete` | Mark todo as incomplete | — | `200 TodoResponse` |

#### Endpoint Details

**GET /api/v1/todos**
- Calls `service.list_todos()`.
- Returns `TodoListResponse(todos=results, count=len(results))` with HTTP 200.

**POST /api/v1/todos**
- Accepts `TodoCreate` in request body.
- Calls `service.create_todo(data)`.
- Returns `TodoResponse.model_validate(todo)` with HTTP 201.

**GET /api/v1/todos/{todo_id}**
- `todo_id` is a path parameter (`int`).
- Calls `service.get_todo(todo_id)`.
- Returns `TodoResponse.model_validate(todo)` with HTTP 200.
- `TodoNotFoundError` is caught by the global exception handler → HTTP 404.

**PUT /api/v1/todos/{todo_id}**
- Accepts `TodoUpdate` in request body.
- Calls `service.update_todo(todo_id, data)`.
- Returns `TodoResponse.model_validate(todo)` with HTTP 200.

**DELETE /api/v1/todos/{todo_id}**
- Calls `service.delete_todo(todo_id)`.
- Returns HTTP 204 with no body (`Response(status_code=204)`).

**PATCH /api/v1/todos/{todo_id}/complete**
- Calls `service.complete_todo(todo_id)`.
- Returns `TodoResponse.model_validate(todo)` with HTTP 200.

**PATCH /api/v1/todos/{todo_id}/uncomplete**
- Calls `service.uncomplete_todo(todo_id)`.
- Returns `TodoResponse.model_validate(todo)` with HTTP 200.

---

### 3.9 Exception Handling

**File:** `backend/app/exceptions.py`

#### `AppException` (Base)

```python
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)
```

#### `TodoNotFoundError`

Raised when a todo with the given ID does not exist. Maps to HTTP 404.

```python
class TodoNotFoundError(AppException):
    def __init__(self, todo_id: int) -> None:
        super().__init__(message=f"Todo with id {todo_id} was not found.", status_code=404)
```

#### `ValidationError`

Raised by the service layer for business-level validation failures (e.g., blank title). Distinct from Pydantic's `RequestValidationError`. Maps to HTTP 422.

```python
class ValidationError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=422)
```

#### Error Response Shape

All handled errors return a consistent JSON body:

```json
{
  "detail": "Todo with id 99 was not found."
}
```

Unhandled exceptions return HTTP 500 with `{"detail": "An unexpected error occurred."}`.

---

### 3.10 Configuration

**File:** `backend/app/config.py`

Use `pydantic-settings` (`BaseSettings`) to load configuration from environment variables and/or a `.env` file.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    APP_ENV: str = "development"
    DEBUG: bool = False
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

settings = Settings()
```

**`.env` file (not committed to source control):**

```
DATABASE_URL=mssql+aioodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\SQLEXPRESS;DATABASE=TodoDB;Trusted_Connection=yes;
APP_ENV=development
DEBUG=True
ALLOWED_ORIGINS=["http://localhost:5173"]
```

Add `.env` to `.gitignore`. Provide a `.env.example` with placeholder values.

#### `requirements.txt`

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
sqlalchemy>=2.0.0
aioodbc>=0.5.0
alembic>=1.13.0
pydantic>=2.7.0
pydantic-settings>=2.2.0
```

#### `requirements-dev.txt`

```
-r requirements.txt
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
```

---

## 4. Frontend Specifications

### 4.1 Technology

| Item | Choice |
|---|---|
| Framework | React 18 |
| Build Tool | Vite 5+ |
| Language | TypeScript (strict mode) |
| HTTP Client | Axios |
| State | Local component state + custom hooks (no Redux in Phase 1) |
| Styling | CSS Modules or plain CSS (no UI library required in Phase 1) |

### 4.2 TypeScript Types

**File:** `frontend/src/types/todo.ts`

```typescript
export interface Todo {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
}

export interface TodoCreate {
  title: string;
  description?: string | null;
}

export interface TodoUpdate {
  title?: string | null;
  description?: string | null;
  is_completed?: boolean | null;
}

export interface TodoListResponse {
  todos: Todo[];
  count: number;
}
```

### 4.3 Axios Instance

**File:** `frontend/src/api/axiosInstance.ts`

- `baseURL`: read from `import.meta.env.VITE_API_BASE_URL` with fallback to `http://localhost:8000`.
- Response interceptor: extracts `error.response.data.detail` for display.
- No auth headers in Phase 1.

### 4.4 Todo API Functions

**File:** `frontend/src/api/todoApi.ts`

```typescript
getAllTodos(): Promise<TodoListResponse>
getTodoById(id: number): Promise<Todo>
createTodo(data: TodoCreate): Promise<Todo>
updateTodo(id: number, data: TodoUpdate): Promise<Todo>
deleteTodo(id: number): Promise<void>
completeTodo(id: number): Promise<Todo>
uncompleteTodo(id: number): Promise<Todo>
```

Each function maps directly to one backend endpoint.

### 4.5 Custom Hook

**File:** `frontend/src/hooks/useTodos.ts`

Manages:
- `todos: Todo[]` state
- `loading: boolean` state
- `error: string | null` state
- Functions: `fetchTodos`, `addTodo`, `editTodo`, `removeTodo`, `toggleComplete`

Fetches todos on mount via `useEffect`.

### 4.6 Components

| Component | Responsibility |
|---|---|
| `TodoPage` | Page-level container; uses `useTodos` hook; renders form and list |
| `TodoList` | Receives `todos` array and callbacks; renders `TodoItem` per entry |
| `TodoItem` | Displays title, description, completion status; provides Edit, Delete, Toggle buttons |
| `TodoForm` | Controlled form for create and edit; accepts optional `initialValues` for edit mode |
| `ErrorMessage` | Displays a dismissible error string |

### 4.7 Vite Configuration

**File:** `frontend/vite.config.ts`

Configure a dev server proxy so requests to `/api` are forwarded to the FastAPI backend, avoiding CORS issues during development:

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
},
```

### 4.8 Environment Variables

**File:** `frontend/.env.development`

```
VITE_API_BASE_URL=http://localhost:8000
```

Prefix all Vite env vars with `VITE_` to expose them to the browser bundle.

---

## 5. Database Design

### 5.1 Database Engine

**SQL Server Express** (local install). The async connection is made via the `aioodbc` driver using the `mssql+aioodbc` SQLAlchemy dialect. Windows Authentication (`Trusted_Connection=yes`) is used for local development.

### 5.2 Schema

**Table: `todos`**

```sql
CREATE TABLE todos (
    id          INT             NOT NULL IDENTITY(1,1),
    title       NVARCHAR(200)   NOT NULL,
    description NVARCHAR(1000)  NULL,
    is_completed BIT            NOT NULL DEFAULT 0,
    created_at  DATETIME2       NOT NULL DEFAULT GETDATE(),
    updated_at  DATETIME2       NOT NULL DEFAULT GETDATE(),

    CONSTRAINT PK_todos PRIMARY KEY (id)
);
```

> Note: The table is created and managed exclusively via Alembic migrations. The SQL above is for reference only.

### 5.3 Column Mapping

| SQL Column | SQL Type | SQLAlchemy Mapped Type | Notes |
|---|---|---|---|
| `id` | `INT IDENTITY` | `Integer` / `Mapped[int]` | Auto-generated PK |
| `title` | `NVARCHAR(200)` | `String(200)` | Required |
| `description` | `NVARCHAR(1000)` | `String(1000)` | Nullable |
| `is_completed` | `BIT` | `Boolean` | Defaults to `False` / `0` |
| `created_at` | `DATETIME2` | `DateTime` | Set by server default |
| `updated_at` | `DATETIME2` | `DateTime` | Set by server default + onupdate |

### 5.4 Indexes

- Primary key index on `id` (automatically created by SQL Server).
- No additional indexes required for Phase 1 (single-user, small dataset).

### 5.5 Database Creation

The database `TodoDB` must be created manually once before running migrations:

```sql
CREATE DATABASE TodoDB;
```

All table structure is then managed via `alembic upgrade head`.

---

## 6. Testing Strategy

### 6.1 Tools

| Tool | Purpose |
|---|---|
| `pytest` | Test runner |
| `pytest-asyncio` | `async def` test support |
| `httpx` (AsyncClient) | HTTP-level integration tests against FastAPI |
| `unittest.mock` | Mocking repository in service unit tests |

Configure `pytest-asyncio` in `pyproject.toml` or `pytest.ini`:

```ini
[pytest]
asyncio_mode = auto
```

### 6.2 Test Layers

#### Layer 1: Repository Integration Tests

**File:** `backend/tests/test_todo_repository.py`

- Use a dedicated test database (e.g., `TodoDB_Test`).
- `conftest.py` creates a test `AsyncEngine`, runs `Base.metadata.create_all`, and yields a scoped `AsyncSession` per test.
- Each test runs inside a transaction that is rolled back after the test (to keep the DB clean without truncation scripts).
- Tests cover: `create`, `get_by_id` (found and not found), `get_all`, `update` (partial field updates), `delete`.

#### Layer 2: Service Unit Tests

**File:** `backend/tests/test_todo_service.py`

- The repository is replaced with a `MagicMock` or `AsyncMock`.
- No database is involved.
- Tests cover all service methods including exception paths:
  - `get_todo` raises `TodoNotFoundError` when repo returns `None`.
  - `create_todo` raises `ValidationError` for blank title.
  - `update_todo` raises `TodoNotFoundError` for missing ID.
  - `update_todo` raises `ValidationError` for blank title in update.
  - `complete_todo` / `uncomplete_todo` raise `TodoNotFoundError` for missing ID.

```python
@pytest.fixture
def mock_repository():
    return AsyncMock(spec=TodoRepository)

@pytest.fixture
def service(mock_repository):
    return TodoService(mock_repository)
```

#### Layer 3: Router Integration Tests

**File:** `backend/tests/test_todo_router.py`

- Use FastAPI's `TestClient` wrapping or `httpx.AsyncClient` with `ASGITransport`.
- Override the `get_db` dependency to inject a test database session.
- Tests cover all 7 endpoints: correct status codes, response shapes, 404 behaviour, validation errors.

```python
@pytest.fixture
async def async_client(override_get_db):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
```

### 6.3 Test Naming Convention

```
test_<method_or_endpoint>_<scenario>
```

Examples:
- `test_create_todo_returns_201_with_valid_data`
- `test_get_todo_returns_404_when_not_found`
- `test_create_todo_raises_validation_error_for_blank_title`

### 6.4 Coverage Target

Aim for >= 80% coverage on `app/services/` and `app/routers/`. Repository coverage is achieved through integration tests. Use `pytest-cov` for reporting.

---

## 7. Development Workflow

### 7.1 Git Branching Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, production-ready code. Protected — no direct pushes. |
| `develop` | Integration branch. All feature branches merge here. |
| `feature/<name>` | Individual feature work. Branched from `develop`. |
| `fix/<name>` | Bug fix branches. Branched from `develop` (or `main` for hotfixes). |
| `chore/<name>` | Non-feature work: dependency updates, config, tooling. |

**Workflow:**
1. Branch from `develop`: `git checkout -b feature/todo-list-endpoint`
2. Commit with conventional commits (see below).
3. Open a pull request targeting `develop`.
4. Squash-merge after review.
5. `develop` is merged to `main` for releases.

### 7.2 Commit Message Conventions

Follow the **Conventional Commits** specification (`https://www.conventionalcommits.org`).

**Format:**

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:**

| Type | When to Use |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `refactor` | Code change that is not a feat or fix |
| `test` | Adding or updating tests |
| `chore` | Build process, dependencies, tooling |
| `docs` | Documentation only changes |
| `style` | Formatting, whitespace (no logic change) |
| `perf` | Performance improvement |

**Examples:**

```
feat(todos): add create todo endpoint
fix(service): raise TodoNotFoundError when todo id is missing
test(repository): add integration tests for get_all
chore(deps): upgrade sqlalchemy to 2.0.30
docs(trd): add phase 1 TRD
```

**Rules:**
- Subject line: imperative mood, max 72 characters, no trailing period.
- Body: explain the *why*, not the *what*, if needed.
- Breaking changes: add `BREAKING CHANGE:` in footer.

### 7.3 `.gitignore` Requirements

```
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
dist/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# Environment
.env
!.env.example

# Frontend
frontend/node_modules/
frontend/dist/
frontend/.env.development.local
frontend/.env.local

# IDE
.vscode/
.idea/
*.suo
*.user

# OS
.DS_Store
Thumbs.db
```

### 7.4 Local Development Setup

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements-dev.txt
cp .env.example .env            # fill in DATABASE_URL
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev                     # starts on http://localhost:5173
```

---

## 8. Instruction File Strategy

Three GitHub Copilot instruction files are maintained under `.github/copilot-instructions/`. Each file provides targeted context for Copilot to generate code consistent with the conventions of this project.

### 8.1 `backend.instructions.md`

**Purpose:** Guide Copilot when writing Python backend code.

**Key content to include:**
- Tech stack: FastAPI, SQLAlchemy 2.x async, Pydantic v2, aioodbc, SQL Server Express.
- Architecture reminder: always use the Route -> Service -> Repository pattern. No database calls directly in routers.
- All functions that touch the DB must be `async def`.
- Repository methods use `flush()`, not `commit()` (commit is handled by `get_db`).
- Use `Mapped` and `mapped_column` (SQLAlchemy 2.x style), not the legacy `Column` style.
- Schemas: use `model_config = ConfigDict(from_attributes=True)` on response schemas.
- Exceptions: service raises `TodoNotFoundError` or `ValidationError`; never raise `HTTPException` inside services.
- Configuration: all settings come from `app.config.settings`, never from hardcoded values.
- Imports: use absolute imports from `app.*`.

### 8.2 `frontend.instructions.md`

**Purpose:** Guide Copilot when writing React/TypeScript frontend code.

**Key content to include:**
- Tech stack: React 18, Vite, TypeScript strict mode, Axios.
- All API calls go through functions in `src/api/todoApi.ts`; never call `axiosInstance` directly from components.
- State management lives in custom hooks (`src/hooks/`), not in components.
- Components receive data and callbacks as props; they do not fetch data themselves.
- Type all props, state, and function return types explicitly — no implicit `any`.
- Use `interface` for object shapes, `type` for unions/aliases.
- Match the `Todo`, `TodoCreate`, `TodoUpdate` interfaces in `src/types/todo.ts` exactly.
- No `console.log` in committed code; use the `error` state exposed by `useTodos`.
- Environment variables: always access via `import.meta.env.VITE_*`.

### 8.3 `testing.instructions.md`

**Purpose:** Guide Copilot when writing pytest tests.

**Key content to include:**
- Use `pytest-asyncio` with `asyncio_mode = auto`; all test functions that are async are automatically treated as async tests.
- Service tests use `AsyncMock(spec=TodoRepository)` — always `spec` the mock to catch attribute typos.
- Repository tests run against the real test database; each test uses a rolled-back transaction to stay isolated.
- Router tests use `httpx.AsyncClient` with `ASGITransport(app=app)` — do not use `TestClient` for async routes.
- Test naming: `test_<method>_<scenario>` in snake_case.
- Always assert both the HTTP status code and the JSON response body shape in router tests.
- For `TodoNotFoundError` paths, assert the status code is `404` and `response.json()["detail"]` contains the todo ID.
- Do not import from `app.database` directly in test files; use fixtures from `conftest.py`.

---

*End of TRD — Phase 1*
