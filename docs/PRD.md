# Product Requirements Document: Todo Management Application

**Version:** 1.0
**Phase:** 1
**Date:** 2026-03-25
**Status:** Draft

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Goals](#2-goals)
3. [Scope](#3-scope)
4. [User Stories](#4-user-stories)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Data Model](#7-data-model)
8. [API Endpoints](#8-api-endpoints)
9. [Error Handling Requirements](#9-error-handling-requirements)
10. [Acceptance Criteria](#10-acceptance-criteria)
11. [Out of Scope](#11-out-of-scope)

---

## 1. Executive Summary

The Todo Management Application is a single-user, browser-based productivity tool that enables a user to create, view, update, complete, and delete personal todo items. Phase 1 establishes the full core lifecycle of a todo item with no authentication and no categorization. The application consists of a React 18 + Vite + TypeScript frontend communicating with a Python FastAPI backend that persists data in SQL Server Express via SQLAlchemy async and Alembic migrations. All backend logic follows a strict Route -> Service -> Repository layered architecture.

---

## 2. Goals

### Primary Goals

- Provide a fast, responsive interface for managing a personal list of todo items.
- Deliver a reliable REST API that covers the complete todo lifecycle (create, read, update, delete, complete, uncomplete).
- Establish a maintainable, layered backend architecture that can be extended in future phases without structural rework.
- Ensure data integrity through consistent validation on both the frontend and backend.

### Secondary Goals

- Keep the deployment footprint minimal: a single backend process and a single frontend build served statically or via a dev server.
- Lay the database migration foundation with Alembic so future schema changes (categories, users) are non-destructive.
- Produce clear API contracts so that the frontend and backend can be developed in parallel against agreed-upon schemas.

---

## 3. Scope

### In Scope (Phase 1)

- A single `todos` table and all CRUD operations against it.
- Seven REST API endpoints covering list, create, retrieve, update, delete, mark complete, and mark uncomplete.
- A React frontend with views for listing todos, creating a new todo, editing an existing todo, and toggling completion status.
- Input validation on both client and server sides.
- Alembic migration scripts for the initial schema.
- Async database access using SQLAlchemy async with an MSSQL (SQL Server Express) connection.
- A Route -> Service -> Repository backend architecture.

### Boundaries

- The application targets a single local user. There is no multi-tenancy or user isolation.
- No authentication or authorization layer is included.
- No category, tag, or grouping functionality is included.

---

## 4. User Stories

| ID   | As a...    | I want to...                                              | So that...                                              |
|------|------------|-----------------------------------------------------------|---------------------------------------------------------|
| US-1 | User       | See a list of all my todo items                           | I have a complete view of my tasks at a glance          |
| US-2 | User       | Create a new todo with a title and optional description   | I can capture a task quickly                            |
| US-3 | User       | View the full details of a single todo                    | I can read the full description when needed             |
| US-4 | User       | Edit the title and description of an existing todo        | I can correct or refine a task                          |
| US-5 | User       | Delete a todo                                             | I can remove tasks that are no longer relevant          |
| US-6 | User       | Mark a todo as complete                                   | I can track which tasks I have finished                 |
| US-7 | User       | Mark a completed todo as incomplete (uncomplete)          | I can reopen a task if it needs more work               |
| US-8 | User       | See when a todo was created and last updated              | I have an audit trail of task history                   |
| US-9 | User       | Filter or distinguish completed todos from active ones    | I can focus on outstanding work                         |

---

## 5. Functional Requirements

### 5.1 Todo Listing

- **FR-1.1** The system must return all todo items stored in the database.
- **FR-1.2** The list must include all fields: `id`, `title`, `description`, `is_completed`, `created_at`, `updated_at`.
- **FR-1.3** The list must be ordered by `created_at` descending by default (newest first).
- **FR-1.4** The frontend must visually distinguish completed todos from incomplete todos (e.g., strikethrough, muted colour, or a completion badge).

### 5.2 Todo Creation

- **FR-2.1** The user must be able to create a todo by providing a `title` (required) and an optional `description`.
- **FR-2.2** The `title` field must not be empty or whitespace-only.
- **FR-2.3** The `title` field must not exceed 255 characters.
- **FR-2.4** The `description` field, if provided, must not exceed 2000 characters.
- **FR-2.5** On successful creation, the system must return the newly created todo including its generated `id`, `created_at`, and `updated_at`.
- **FR-2.6** A new todo must default to `is_completed = false`.

### 5.3 Todo Retrieval

- **FR-3.1** The system must return the full details of a single todo identified by its `id`.
- **FR-3.2** If no todo exists for the given `id`, the system must return a 404 response.

### 5.4 Todo Update

- **FR-4.1** The user must be able to update the `title` and/or `description` of an existing todo.
- **FR-4.2** The update operation must accept a partial payload; fields not provided must remain unchanged.
- **FR-4.3** The same validation rules as creation apply to updated field values (FR-2.2, FR-2.3, FR-2.4).
- **FR-4.4** On a successful update, `updated_at` must be refreshed to the current UTC timestamp.
- **FR-4.5** The `is_completed` field must not be modifiable through the general update endpoint; completion state is managed exclusively via the complete and uncomplete endpoints.
- **FR-4.6** If no todo exists for the given `id`, the system must return a 404 response.

### 5.5 Todo Deletion

- **FR-5.1** The user must be able to permanently delete a todo by its `id`.
- **FR-5.2** On successful deletion, the system must return a 204 No Content response.
- **FR-5.3** If no todo exists for the given `id`, the system must return a 404 response.

### 5.6 Mark Complete

- **FR-6.1** The user must be able to mark an incomplete todo as complete via a dedicated endpoint.
- **FR-6.2** Calling complete on a todo that is already completed must be idempotent: the system returns 200 with the current state without raising an error.
- **FR-6.3** On a successful transition, `is_completed` must be set to `true` and `updated_at` must be refreshed.

### 5.7 Mark Uncomplete

- **FR-7.1** The user must be able to mark a completed todo as incomplete via a dedicated endpoint.
- **FR-7.2** Calling uncomplete on a todo that is already incomplete must be idempotent: the system returns 200 with the current state without raising an error.
- **FR-7.3** On a successful transition, `is_completed` must be set to `false` and `updated_at` must be refreshed.

### 5.8 Frontend Behaviour

- **FR-8.1** The frontend must display a loading indicator while any API request is in flight.
- **FR-8.2** The frontend must display a human-readable error message when an API request fails.
- **FR-8.3** All forms must validate input client-side before submitting to the API.
- **FR-8.4** After a successful create, update, delete, complete, or uncomplete action, the todo list must reflect the change without requiring a manual page refresh.

---

## 6. Non-Functional Requirements

### 6.1 Performance

- **NFR-1.1** API responses for list, create, get, update, delete, complete, and uncomplete must complete within 500 ms under normal single-user load.
- **NFR-1.2** The frontend initial page load (after build) must achieve a Largest Contentful Paint (LCP) of under 2.5 seconds on a modern desktop browser over localhost.

### 6.2 Reliability

- **NFR-2.1** The backend must handle unexpected exceptions gracefully and never expose raw stack traces or internal database error messages to the client.
- **NFR-2.2** All database operations must be executed within async transactions; partial writes on failure must be rolled back automatically.

### 6.3 Maintainability

- **NFR-3.1** The backend must follow a strict three-layer architecture: **Route** (HTTP request/response, input parsing, response serialization) -> **Service** (business logic, validation) -> **Repository** (database access via SQLAlchemy async). No layer may bypass another.
- **NFR-3.2** Database schema changes must be managed exclusively through Alembic migration scripts; direct DDL modifications to the database are prohibited.
- **NFR-3.3** All backend code must be typed with Python type hints. All frontend code must be typed with TypeScript (strict mode enabled; no `any` unless explicitly justified).
- **NFR-3.4** Environment-specific configuration (database URL, CORS origins) must be managed via environment variables or a `.env` file, never hardcoded.

### 6.4 Compatibility

- **NFR-4.1** The frontend must function correctly in the latest stable versions of Chrome, Firefox, and Edge.
- **NFR-4.2** The backend must run on Python 3.11 or later.
- **NFR-4.3** The frontend must be built with Node.js 20 LTS or later.

### 6.5 Security (Baseline)

- **NFR-5.1** The API must enable CORS restricted to the configured frontend origin(s).
- **NFR-5.2** All database queries must use parameterised statements via the SQLAlchemy ORM; raw string interpolation into SQL is prohibited.
- **NFR-5.3** User-supplied strings must be stored as-is and HTML-escaped at the point of rendering in the frontend to prevent XSS.

### 6.6 Usability

- **NFR-6.1** The frontend UI must be usable without a mouse (keyboard navigation for all interactive controls).
- **NFR-6.2** Form validation errors must be displayed inline adjacent to the relevant field.

---

## 7. Data Model

### 7.1 Entity: Todo

**Table name:** `todos`

| Column         | Type             | Constraints                                          | Description                                         |
|----------------|------------------|------------------------------------------------------|-----------------------------------------------------|
| `id`           | INTEGER          | PRIMARY KEY, IDENTITY (auto-increment), NOT NULL     | Unique surrogate identifier for the todo item       |
| `title`        | NVARCHAR(255)    | NOT NULL                                             | Short descriptive title of the todo item            |
| `description`  | NVARCHAR(2000)   | NULL                                                 | Optional detailed description of the todo item      |
| `is_completed` | BIT              | NOT NULL, DEFAULT 0                                  | Completion flag; 0 = incomplete, 1 = complete       |
| `created_at`   | DATETIME2        | NOT NULL, DEFAULT GETUTCDATE()                       | UTC timestamp of when the record was created        |
| `updated_at`   | DATETIME2        | NOT NULL, DEFAULT GETUTCDATE()                       | UTC timestamp of the most recent update to the row  |

### 7.2 Notes

- `id` is auto-incremented by the database; clients must not supply it on creation.
- `created_at` is set once at insert time and must never be modified thereafter.
- `updated_at` must be updated by the application layer (SQLAlchemy event or service logic) on every write operation that modifies the row.
- `NVARCHAR` is used for `title` and `description` to support Unicode characters under SQL Server Express.
- `DATETIME2` is used in preference to `DATETIME` for its greater precision and range.

### 7.3 SQLAlchemy Model (Reference)

```python
class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, default=func.now(), onupdate=func.now())
```

---

## 8. API Endpoints

**Base path:** `/api/v1`
**Content-Type:** `application/json` for all request and response bodies.

---

### 8.1 List Todos

| Attribute     | Value                  |
|---------------|------------------------|
| Method        | GET                    |
| Path          | `/api/v1/todos`        |
| Auth Required | No                     |

**Query Parameters:** None (Phase 1).

**Success Response — 200 OK**

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false,
    "created_at": "2026-03-25T09:00:00Z",
    "updated_at": "2026-03-25T09:00:00Z"
  }
]
```

Returns an empty array `[]` when no todos exist.

---

### 8.2 Create Todo

| Attribute     | Value                  |
|---------------|------------------------|
| Method        | POST                   |
| Path          | `/api/v1/todos`        |
| Auth Required | No                     |

**Request Body**

```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

| Field         | Type   | Required | Validation                          |
|---------------|--------|----------|-------------------------------------|
| `title`       | string | Yes      | Non-empty, max 255 characters       |
| `description` | string | No       | Max 2000 characters; omit or null   |

**Success Response — 201 Created**

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2026-03-25T09:00:00Z",
  "updated_at": "2026-03-25T09:00:00Z"
}
```

**Error Responses:** 422 Unprocessable Entity (validation failure).

---

### 8.3 Get Todo

| Attribute     | Value                      |
|---------------|----------------------------|
| Method        | GET                        |
| Path          | `/api/v1/todos/{todo_id}`  |
| Auth Required | No                         |

**Path Parameters**

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `todo_id` | integer | The todo's unique ID |

**Success Response — 200 OK**

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2026-03-25T09:00:00Z",
  "updated_at": "2026-03-25T09:00:00Z"
}
```

**Error Responses:** 404 Not Found.

---

### 8.4 Update Todo

| Attribute     | Value                      |
|---------------|----------------------------|
| Method        | PATCH                      |
| Path          | `/api/v1/todos/{todo_id}`  |
| Auth Required | No                         |

**Path Parameters**

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `todo_id` | integer | The todo's unique ID |

**Request Body** (all fields optional; at least one must be present)

```json
{
  "title": "Buy groceries and toiletries",
  "description": "Milk, eggs, bread, shampoo"
}
```

| Field         | Type   | Required | Validation                          |
|---------------|--------|----------|-------------------------------------|
| `title`       | string | No       | Non-empty, max 255 characters       |
| `description` | string | No       | Max 2000 characters; null clears it |

**Success Response — 200 OK** — Returns the full updated todo object.

**Error Responses:** 404 Not Found, 422 Unprocessable Entity.

---

### 8.5 Delete Todo

| Attribute     | Value                      |
|---------------|----------------------------|
| Method        | DELETE                     |
| Path          | `/api/v1/todos/{todo_id}`  |
| Auth Required | No                         |

**Path Parameters**

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `todo_id` | integer | The todo's unique ID |

**Success Response — 204 No Content** — Empty body.

**Error Responses:** 404 Not Found.

---

### 8.6 Complete Todo

| Attribute     | Value                               |
|---------------|-------------------------------------|
| Method        | PATCH                               |
| Path          | `/api/v1/todos/{todo_id}/complete`  |
| Auth Required | No                                  |

**Path Parameters**

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `todo_id` | integer | The todo's unique ID |

**Request Body:** None.

**Success Response — 200 OK** — Returns the full updated todo object with `is_completed: true`.

**Error Responses:** 404 Not Found.

---

### 8.7 Uncomplete Todo

| Attribute     | Value                                 |
|---------------|---------------------------------------|
| Method        | PATCH                                 |
| Path          | `/api/v1/todos/{todo_id}/uncomplete`  |
| Auth Required | No                                    |

**Path Parameters**

| Parameter | Type    | Description          |
|-----------|---------|----------------------|
| `todo_id` | integer | The todo's unique ID |

**Request Body:** None.

**Success Response — 200 OK** — Returns the full updated todo object with `is_completed: false`.

**Error Responses:** 404 Not Found.

---

### 8.8 Endpoint Summary Table

| #  | Method | Path                                  | Description        | Success Code |
|----|--------|---------------------------------------|--------------------|--------------|
| 1  | GET    | `/api/v1/todos`                       | List all todos     | 200          |
| 2  | POST   | `/api/v1/todos`                       | Create a todo      | 201          |
| 3  | GET    | `/api/v1/todos/{todo_id}`             | Get a todo         | 200          |
| 4  | PATCH  | `/api/v1/todos/{todo_id}`             | Update a todo      | 200          |
| 5  | DELETE | `/api/v1/todos/{todo_id}`             | Delete a todo      | 204          |
| 6  | PATCH  | `/api/v1/todos/{todo_id}/complete`    | Mark complete      | 200          |
| 7  | PATCH  | `/api/v1/todos/{todo_id}/uncomplete`  | Mark uncomplete    | 200          |

---

## 9. Error Handling Requirements

### 9.1 Standard Error Response Schema

All error responses must use the following JSON structure:

```json
{
  "detail": "A human-readable description of the error."
}
```

For validation errors (422), FastAPI's default Pydantic error format is acceptable and must include the `detail` array identifying each invalid field and the reason.

### 9.2 HTTP Status Code Usage

| Status Code                  | When to Use                                                                                 |
|------------------------------|---------------------------------------------------------------------------------------------|
| 200 OK                       | Successful GET, PATCH (update/complete/uncomplete)                                          |
| 201 Created                  | Successful POST (todo created)                                                              |
| 204 No Content               | Successful DELETE                                                                           |
| 400 Bad Request              | Malformed request body (non-JSON, wrong content-type)                                       |
| 404 Not Found                | The requested `todo_id` does not exist in the database                                      |
| 422 Unprocessable Entity     | Request body is valid JSON but fails schema or business validation rules                    |
| 500 Internal Server Error    | Unhandled server-side exception; must not leak internal details to the client               |

### 9.3 Backend Error Handling Rules

- **EH-1** The Route layer must not catch exceptions that belong to the Service or Repository layer; a global exception handler registered on the FastAPI app must handle unrecognised exceptions and return 500.
- **EH-2** The Service layer must raise a typed `TodoNotFoundError` (or equivalent HTTP exception) when a requested todo does not exist. The Route layer converts this to a 404 response.
- **EH-3** The Repository layer must propagate database-level exceptions upward; it must not silently swallow errors.
- **EH-4** No exception handler must include a raw Python traceback, SQLAlchemy error detail, or database connection string in the HTTP response body.
- **EH-5** All unhandled exceptions must be logged server-side with full traceback for debugging.

### 9.4 Frontend Error Handling Rules

- **EH-6** The frontend must parse the `detail` field from error responses and display it to the user in a visible, non-blocking notification (e.g., a toast or inline alert).
- **EH-7** Network errors (no response from server) must display a generic "Unable to connect to the server. Please try again." message.
- **EH-8** The frontend must not display raw HTTP status codes to the user; all errors must be presented in plain language.

---

## 10. Acceptance Criteria

### AC-1: List Todos

- Given the database contains 3 todos, when the user visits the application, then all 3 todos are displayed.
- Given the database is empty, when the user visits the application, then an empty state message is shown (e.g., "No todos yet. Create one to get started.").

### AC-2: Create Todo

- Given the user submits a valid title, when the form is submitted, then a new todo appears at the top of the list with `is_completed = false` and the correct title.
- Given the user submits an empty title, when the form is submitted, then the form displays a validation error and no API call is made.
- Given the user submits a title exceeding 255 characters, then the form displays a validation error and no API call is made.
- Given a valid POST request reaches the API, then the API returns 201 with the created todo including `id`, `created_at`, and `updated_at`.

### AC-3: Get Todo

- Given a valid `todo_id`, when the GET endpoint is called, then 200 is returned with the full todo object.
- Given a non-existent `todo_id`, when the GET endpoint is called, then 404 is returned with a `detail` message.

### AC-4: Update Todo

- Given the user edits a todo's title and saves, then the updated title is reflected in the list and the `updated_at` timestamp is newer than `created_at`.
- Given the user submits an update with an empty title, then 422 is returned and the record is unchanged.
- Given a PATCH request for a non-existent `todo_id`, then 404 is returned.

### AC-5: Delete Todo

- Given the user deletes a todo, then it is removed from the list immediately and a DELETE to the API returns 204.
- Given a DELETE request for a non-existent `todo_id`, then 404 is returned.

### AC-6: Complete Todo

- Given an incomplete todo, when the user marks it complete, then `is_completed` becomes `true`, the UI reflects the completed state, and `updated_at` is refreshed.
- Given an already-complete todo, when the complete endpoint is called again, then 200 is returned with the current state (idempotent).

### AC-7: Uncomplete Todo

- Given a completed todo, when the user marks it incomplete, then `is_completed` becomes `false`, the UI reflects the active state, and `updated_at` is refreshed.
- Given an already-incomplete todo, when the uncomplete endpoint is called again, then 200 is returned with the current state (idempotent).

### AC-8: Error Handling

- Given the server returns a 500, then the frontend displays a user-friendly error message without exposing internal details.
- Given the frontend cannot reach the backend, then a "Unable to connect" message is displayed.

### AC-9: Architecture

- Given a code review, the Route layer must contain no SQLAlchemy queries or direct business logic beyond request parsing and response serialization.
- Given a code review, the Repository layer must contain no business validation logic.
- Given a code review, all database schema changes must be present as Alembic migration scripts and must be reproducible from a clean database via `alembic upgrade head`.

---

## 11. Out of Scope

The following features and concerns are explicitly excluded from Phase 1. They may be addressed in future phases but must not influence the Phase 1 architecture or data model in ways that would require breaking changes.

### 11.1 Categories and Tagging

- No category, label, tag, or grouping entity will be created.
- No foreign keys referencing a categories table will be added to the `todos` table.
- The UI will have no filtering, grouping, or navigation by category.

### 11.2 Authentication and Authorization

- There is no login, logout, session management, or token-based authentication.
- There are no user accounts, roles, or permission checks.
- All API endpoints are publicly accessible on the local network without credentials.

### 11.3 Multi-User Support

- The application is designed for a single user only.
- There is no `user_id` column or tenant isolation on the `todos` table.
- No concurrency control (optimistic locking, ETags) is implemented.

### 11.4 Additional Features (Future Phases)

- Due dates, reminders, and notifications.
- Priority levels or ordering by priority.
- Subtasks or nested todos.
- Search and full-text filtering.
- Pagination and sorting options on the list endpoint.
- Bulk operations (bulk delete, bulk complete).
- Audit history or soft deletes.
- File or image attachments.
- Export (CSV, JSON).
- Offline support or service workers.
- Mobile-native application.

---

*End of PRD — Phase 1*
