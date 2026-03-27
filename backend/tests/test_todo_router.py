"""Integration tests for Todo API endpoints via AsyncClient."""

import pytest
from httpx import AsyncClient


class TestListTodos:
    """Tests for GET /api/v1/todos."""

    async def test_list_todos_when_empty(self, client: AsyncClient) -> None:
        """Return an empty list with count 0 when no todos exist."""
        response = await client.get("/api/v1/todos")

        assert response.status_code == 200
        body = response.json()
        assert body["todos"] == []
        assert body["count"] == 0

    async def test_list_todos_when_todos_exist(self, client: AsyncClient) -> None:
        """Return all todos with correct count."""
        await client.post("/api/v1/todos", json={"title": "First"})
        await client.post("/api/v1/todos", json={"title": "Second"})

        response = await client.get("/api/v1/todos")

        assert response.status_code == 200
        body = response.json()
        assert body["count"] == 2
        assert len(body["todos"]) == 2


class TestCreateTodo:
    """Tests for POST /api/v1/todos."""

    async def test_create_todo_when_valid(self, client: AsyncClient) -> None:
        """Create a todo and return 201 with the created resource."""
        response = await client.post(
            "/api/v1/todos",
            json={"title": "Buy groceries", "description": "Milk, eggs"},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Buy groceries"
        assert body["description"] == "Milk, eggs"
        assert body["is_completed"] is False
        assert "id" in body
        assert "created_at" in body
        assert "updated_at" in body

    async def test_create_todo_when_no_description(self, client: AsyncClient) -> None:
        """Create a todo with no description."""
        response = await client.post(
            "/api/v1/todos", json={"title": "Simple task"}
        )

        assert response.status_code == 201
        assert response.json()["description"] is None

    async def test_create_todo_when_empty_title(self, client: AsyncClient) -> None:
        """Return 422 when title is empty."""
        response = await client.post("/api/v1/todos", json={"title": ""})

        assert response.status_code == 422

    async def test_create_todo_when_whitespace_title(
        self, client: AsyncClient
    ) -> None:
        """Return 422 when title is whitespace only."""
        response = await client.post("/api/v1/todos", json={"title": "   "})

        assert response.status_code == 422


class TestGetTodo:
    """Tests for GET /api/v1/todos/{todo_id}."""

    async def test_get_todo_when_exists(self, client: AsyncClient) -> None:
        """Return the todo when it exists."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "Existing"}
        )
        todo_id = create_resp.json()["id"]

        response = await client.get(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 200
        assert response.json()["title"] == "Existing"

    async def test_get_todo_when_not_found(self, client: AsyncClient) -> None:
        """Return 404 when the todo does not exist."""
        response = await client.get("/api/v1/todos/999")

        assert response.status_code == 404
        assert "detail" in response.json()


class TestUpdateTodo:
    """Tests for PATCH /api/v1/todos/{todo_id}."""

    async def test_update_todo_when_valid(self, client: AsyncClient) -> None:
        """Update the todo and return the updated resource."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "Original"}
        )
        todo_id = create_resp.json()["id"]

        response = await client.patch(
            f"/api/v1/todos/{todo_id}",
            json={"title": "Updated title"},
        )

        assert response.status_code == 200
        assert response.json()["title"] == "Updated title"

    async def test_update_todo_when_not_found(self, client: AsyncClient) -> None:
        """Return 404 when the todo does not exist."""
        response = await client.patch(
            "/api/v1/todos/999", json={"title": "Nope"}
        )

        assert response.status_code == 404

    async def test_update_todo_when_partial(self, client: AsyncClient) -> None:
        """Update only provided fields, leaving others unchanged."""
        create_resp = await client.post(
            "/api/v1/todos",
            json={"title": "Full", "description": "Original desc"},
        )
        todo_id = create_resp.json()["id"]

        response = await client.patch(
            f"/api/v1/todos/{todo_id}",
            json={"description": "New desc"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Full"
        assert body["description"] == "New desc"


class TestDeleteTodo:
    """Tests for DELETE /api/v1/todos/{todo_id}."""

    async def test_delete_todo_when_exists(self, client: AsyncClient) -> None:
        """Delete the todo and return 204."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "To delete"}
        )
        todo_id = create_resp.json()["id"]

        response = await client.delete(f"/api/v1/todos/{todo_id}")

        assert response.status_code == 204

        get_resp = await client.get(f"/api/v1/todos/{todo_id}")
        assert get_resp.status_code == 404

    async def test_delete_todo_when_not_found(self, client: AsyncClient) -> None:
        """Return 404 when the todo does not exist."""
        response = await client.delete("/api/v1/todos/999")

        assert response.status_code == 404


class TestCompleteTodo:
    """Tests for PATCH /api/v1/todos/{todo_id}/complete."""

    async def test_complete_todo_when_incomplete(
        self, client: AsyncClient
    ) -> None:
        """Mark an incomplete todo as completed."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "Task"}
        )
        todo_id = create_resp.json()["id"]

        response = await client.patch(f"/api/v1/todos/{todo_id}/complete")

        assert response.status_code == 200
        assert response.json()["is_completed"] is True

    async def test_complete_todo_when_already_completed(
        self, client: AsyncClient
    ) -> None:
        """Return 200 idempotently when already completed."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "Task"}
        )
        todo_id = create_resp.json()["id"]
        await client.patch(f"/api/v1/todos/{todo_id}/complete")

        response = await client.patch(f"/api/v1/todos/{todo_id}/complete")

        assert response.status_code == 200
        assert response.json()["is_completed"] is True

    async def test_complete_todo_when_not_found(
        self, client: AsyncClient
    ) -> None:
        """Return 404 when the todo does not exist."""
        response = await client.patch("/api/v1/todos/999/complete")

        assert response.status_code == 404


class TestUncompleteTodo:
    """Tests for PATCH /api/v1/todos/{todo_id}/uncomplete."""

    async def test_uncomplete_todo_when_completed(
        self, client: AsyncClient
    ) -> None:
        """Mark a completed todo as incomplete."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "Task"}
        )
        todo_id = create_resp.json()["id"]
        await client.patch(f"/api/v1/todos/{todo_id}/complete")

        response = await client.patch(f"/api/v1/todos/{todo_id}/uncomplete")

        assert response.status_code == 200
        assert response.json()["is_completed"] is False

    async def test_uncomplete_todo_when_already_incomplete(
        self, client: AsyncClient
    ) -> None:
        """Return 200 idempotently when already incomplete."""
        create_resp = await client.post(
            "/api/v1/todos", json={"title": "Task"}
        )
        todo_id = create_resp.json()["id"]

        response = await client.patch(f"/api/v1/todos/{todo_id}/uncomplete")

        assert response.status_code == 200
        assert response.json()["is_completed"] is False

    async def test_uncomplete_todo_when_not_found(
        self, client: AsyncClient
    ) -> None:
        """Return 404 when the todo does not exist."""
        response = await client.patch("/api/v1/todos/999/uncomplete")

        assert response.status_code == 404
