"""Unit tests for TodoRepository."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate


@pytest.fixture()
def repo() -> TodoRepository:
    """Return a TodoRepository instance."""
    return TodoRepository()


async def test_get_by_id_when_todo_exists(
    session: AsyncSession, repo: TodoRepository, sample_todo: Todo
) -> None:
    """Verify get_by_id returns the todo when it exists."""
    result = await repo.get_by_id(session, sample_todo.id)
    assert result is not None
    assert result.id == sample_todo.id
    assert result.title == "Test Todo"


async def test_get_by_id_when_todo_not_found_returns_none(
    session: AsyncSession, repo: TodoRepository
) -> None:
    """Verify get_by_id returns None for a nonexistent ID."""
    result = await repo.get_by_id(session, 9999)
    assert result is None


async def test_get_all_when_todos_exist(
    session: AsyncSession, repo: TodoRepository, sample_todo: Todo
) -> None:
    """Verify get_all returns all existing todos."""
    todos = await repo.get_all(session)
    assert len(todos) >= 1
    assert any(t.id == sample_todo.id for t in todos)


async def test_get_all_when_empty_returns_empty_list(
    session: AsyncSession, repo: TodoRepository
) -> None:
    """Verify get_all returns empty list when no todos exist."""
    todos = await repo.get_all(session)
    assert todos == []


async def test_create_when_valid_data_returns_todo(
    session: AsyncSession, repo: TodoRepository
) -> None:
    """Verify create returns a new todo with correct fields."""
    data = TodoCreate(title="New Todo", description="Some description")
    todo = await repo.create(session, data)
    assert todo.id is not None
    assert todo.title == "New Todo"
    assert todo.description == "Some description"
    assert todo.is_completed is False


async def test_update_when_todo_exists_returns_updated(
    session: AsyncSession, repo: TodoRepository, sample_todo: Todo
) -> None:
    """Verify update modifies and returns the updated todo."""
    data = TodoUpdate(title="Updated Title")
    updated = await repo.update(session, sample_todo, data)
    assert updated.title == "Updated Title"
    assert updated.id == sample_todo.id


async def test_delete_when_todo_exists_removes_record(
    session: AsyncSession, repo: TodoRepository, sample_todo: Todo
) -> None:
    """Verify delete removes the todo from the database."""
    await repo.delete(session, sample_todo)
    result = await repo.get_by_id(session, sample_todo.id)
    assert result is None
