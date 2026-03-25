"""Integration tests for the Todo API endpoints."""

import pytest
from httpx import AsyncClient


async def test_create_todo_returns_201(client: AsyncClient) -> None:
    """Verify creating a todo returns 201 with correct data."""
    response = await client.post(
        "/api/v1/todos", json={"title": "Buy groceries", "description": "Milk, eggs"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs"
    assert data["is_completed"] is False
    assert "id" in data


async def test_create_todo_with_empty_title_returns_422(client: AsyncClient) -> None:
    """Verify creating a todo with empty title returns 422."""
    response = await client.post("/api/v1/todos", json={"title": ""})
    assert response.status_code == 422


async def test_get_todo_returns_200(client: AsyncClient) -> None:
    """Verify getting an existing todo returns 200."""
    create_resp = await client.post("/api/v1/todos", json={"title": "Read book"})
    todo_id = create_resp.json()["id"]
    response = await client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read book"


async def test_get_todo_not_found_returns_404(client: AsyncClient) -> None:
    """Verify getting a nonexistent todo returns 404."""
    response = await client.get("/api/v1/todos/9999")
    assert response.status_code == 404


async def test_update_todo_returns_200(client: AsyncClient) -> None:
    """Verify updating a todo returns 200 with updated data."""
    create_resp = await client.post("/api/v1/todos", json={"title": "Old title"})
    todo_id = create_resp.json()["id"]
    response = await client.put(
        f"/api/v1/todos/{todo_id}", json={"title": "New title"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


async def test_delete_todo_returns_204(client: AsyncClient) -> None:
    """Verify deleting a todo returns 204."""
    create_resp = await client.post("/api/v1/todos", json={"title": "To delete"})
    todo_id = create_resp.json()["id"]
    response = await client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 204


async def test_complete_todo_returns_200(client: AsyncClient) -> None:
    """Verify marking a todo complete returns 200."""
    create_resp = await client.post("/api/v1/todos", json={"title": "Complete me"})
    todo_id = create_resp.json()["id"]
    response = await client.patch(f"/api/v1/todos/{todo_id}/complete")
    assert response.status_code == 200
    assert response.json()["is_completed"] is True


async def test_uncomplete_todo_returns_200(client: AsyncClient) -> None:
    """Verify marking a todo incomplete returns 200."""
    create_resp = await client.post("/api/v1/todos", json={"title": "Uncomplete me"})
    todo_id = create_resp.json()["id"]
    await client.patch(f"/api/v1/todos/{todo_id}/complete")
    response = await client.patch(f"/api/v1/todos/{todo_id}/uncomplete")
    assert response.status_code == 200
    assert response.json()["is_completed"] is False


async def test_list_todos_returns_200(client: AsyncClient) -> None:
    """Verify listing todos returns 200 with all created items."""
    await client.post("/api/v1/todos", json={"title": "Todo 1"})
    await client.post("/api/v1/todos", json={"title": "Todo 2"})
    response = await client.get("/api/v1/todos")
    assert response.status_code == 200
    assert len(response.json()) >= 2


async def test_delete_todo_not_found_returns_404(client: AsyncClient) -> None:
    """Verify deleting a nonexistent todo returns 404."""
    response = await client.delete("/api/v1/todos/9999")
    assert response.status_code == 404


async def test_create_todo_with_whitespace_only_title_returns_422(
    client: AsyncClient,
) -> None:
    """Verify whitespace-only title is rejected with 422."""
    response = await client.post("/api/v1/todos", json={"title": "   "})
    assert response.status_code == 422


async def test_create_todo_with_title_exceeding_max_length_returns_422(
    client: AsyncClient,
) -> None:
    """Verify title exceeding 200 chars is rejected with 422."""
    response = await client.post("/api/v1/todos", json={"title": "a" * 201})
    assert response.status_code == 422


async def test_create_todo_with_description_exceeding_max_length_returns_422(
    client: AsyncClient,
) -> None:
    """Verify description exceeding 1000 chars is rejected with 422."""
    response = await client.post(
        "/api/v1/todos", json={"title": "Valid", "description": "a" * 1001}
    )
    assert response.status_code == 422


async def test_complete_todo_already_completed_returns_200_idempotent(
    client: AsyncClient,
) -> None:
    """Verify completing an already-completed todo is idempotent."""
    create_resp = await client.post("/api/v1/todos", json={"title": "Idempotent"})
    todo_id = create_resp.json()["id"]
    await client.patch(f"/api/v1/todos/{todo_id}/complete")
    response = await client.patch(f"/api/v1/todos/{todo_id}/complete")
    assert response.status_code == 200
    assert response.json()["is_completed"] is True


async def test_get_todos_returns_todos_ordered_by_created_at_desc(
    client: AsyncClient,
) -> None:
    """Verify todos are returned in descending creation order."""
    await client.post("/api/v1/todos", json={"title": "First"})
    await client.post("/api/v1/todos", json={"title": "Second"})
    await client.post("/api/v1/todos", json={"title": "Third"})
    response = await client.get("/api/v1/todos")
    todos = response.json()
    assert len(todos) >= 3
    dates = [t["created_at"] for t in todos]
    assert dates == sorted(dates, reverse=True)
