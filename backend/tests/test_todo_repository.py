"""Integration tests for TodoRepository against SQLite in-memory database."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate


@pytest.fixture
def repository() -> TodoRepository:
    """Create a TodoRepository instance."""
    return TodoRepository()


class TestGetById:
    """Tests for TodoRepository.get_by_id."""

    async def test_get_by_id_when_exists(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Return the todo when a matching ID exists."""
        todo = Todo(title="Test todo", description="A description")
        db_session.add(todo)
        await db_session.flush()
        await db_session.refresh(todo)

        result = await repository.get_by_id(db_session, todo.id)

        assert result is not None
        assert result.id == todo.id
        assert result.title == "Test todo"

    async def test_get_by_id_when_not_exists(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Return None when no todo matches the given ID."""
        result = await repository.get_by_id(db_session, 999)

        assert result is None


class TestGetAll:
    """Tests for TodoRepository.get_all."""

    async def test_get_all_when_empty(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Return an empty list when no todos exist."""
        result = await repository.get_all(db_session)

        assert result == []

    async def test_get_all_when_multiple_exist(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Return all todos ordered by created_at descending."""
        todo1 = Todo(title="First")
        todo2 = Todo(title="Second")
        db_session.add_all([todo1, todo2])
        await db_session.flush()

        result = await repository.get_all(db_session)

        assert len(result) == 2


class TestCreate:
    """Tests for TodoRepository.create."""

    async def test_create_when_valid_data(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Create and return a todo with generated ID and timestamps."""
        data = TodoCreate(title="New todo", description="Details")

        result = await repository.create(db_session, data)

        assert result.id is not None
        assert result.title == "New todo"
        assert result.description == "Details"
        assert result.is_completed is False
        assert result.created_at is not None
        assert result.updated_at is not None

    async def test_create_when_no_description(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Create a todo with None description."""
        data = TodoCreate(title="No desc")

        result = await repository.create(db_session, data)

        assert result.description is None


class TestUpdate:
    """Tests for TodoRepository.update."""

    async def test_update_when_title_changed(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Update only the title and leave other fields intact."""
        todo = Todo(title="Original", description="Desc")
        db_session.add(todo)
        await db_session.flush()
        await db_session.refresh(todo)

        data = TodoUpdate(title="Updated")
        result = await repository.update(db_session, todo, data)

        assert result.title == "Updated"
        assert result.description == "Desc"

    async def test_update_when_completed(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Update is_completed flag."""
        todo = Todo(title="Task")
        db_session.add(todo)
        await db_session.flush()
        await db_session.refresh(todo)

        data = TodoUpdate(is_completed=True)
        result = await repository.update(db_session, todo, data)

        assert result.is_completed is True


class TestDelete:
    """Tests for TodoRepository.delete."""

    async def test_delete_when_exists(
        self, db_session: AsyncSession, repository: TodoRepository
    ) -> None:
        """Delete the todo so it no longer exists in the database."""
        todo = Todo(title="To delete")
        db_session.add(todo)
        await db_session.flush()
        await db_session.refresh(todo)
        todo_id = todo.id

        await repository.delete(db_session, todo)
        await db_session.flush()

        result = await repository.get_by_id(db_session, todo_id)
        assert result is None
