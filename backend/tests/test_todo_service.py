"""Unit tests for TodoService with mocked repository."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.exceptions import TodoNotFoundError
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services.todo_service import TodoService


@pytest.fixture
def mock_repository() -> MagicMock:
    """Create a mock TodoRepository with async methods."""
    repo = MagicMock()
    repo.get_by_id = AsyncMock()
    repo.get_all = AsyncMock()
    repo.create = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repository: MagicMock) -> TodoService:
    """Create a TodoService with a mocked repository."""
    return TodoService(repository=mock_repository)


@pytest.fixture
def mock_session() -> AsyncMock:
    """Create a mock AsyncSession."""
    return AsyncMock()


def _make_todo(
    todo_id: int = 1,
    title: str = "Test",
    description: str | None = None,
    is_completed: bool = False,
) -> Todo:
    """Create a Todo instance for testing."""
    todo = Todo(title=title, description=description, is_completed=is_completed)
    todo.id = todo_id
    return todo


class TestGetTodo:
    """Tests for TodoService.get_todo."""

    async def test_get_todo_when_exists(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Return the todo when it exists."""
        expected = _make_todo()
        mock_repository.get_by_id.return_value = expected

        result = await service.get_todo(mock_session, 1)

        assert result == expected
        mock_repository.get_by_id.assert_awaited_once_with(mock_session, 1)

    async def test_get_todo_when_not_found(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Raise TodoNotFoundError when the todo does not exist."""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(TodoNotFoundError):
            await service.get_todo(mock_session, 999)


class TestListTodos:
    """Tests for TodoService.list_todos."""

    async def test_list_todos_when_empty(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Return an empty list when no todos exist."""
        mock_repository.get_all.return_value = []

        result = await service.list_todos(mock_session)

        assert result == []

    async def test_list_todos_when_multiple_exist(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Return all todos from the repository."""
        todos = [_make_todo(1, "A"), _make_todo(2, "B")]
        mock_repository.get_all.return_value = todos

        result = await service.list_todos(mock_session)

        assert len(result) == 2


class TestCreateTodo:
    """Tests for TodoService.create_todo."""

    async def test_create_todo_when_valid(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Create and return a new todo."""
        data = TodoCreate(title="New todo", description="Details")
        expected = _make_todo(title="New todo", description="Details")
        mock_repository.create.return_value = expected

        result = await service.create_todo(mock_session, data)

        assert result.title == "New todo"
        mock_repository.create.assert_awaited_once_with(mock_session, data)


class TestUpdateTodo:
    """Tests for TodoService.update_todo."""

    async def test_update_todo_when_exists(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Update and return the todo when it exists."""
        existing = _make_todo()
        mock_repository.get_by_id.return_value = existing
        data = TodoUpdate(title="Updated")
        updated = _make_todo(title="Updated")
        mock_repository.update.return_value = updated

        result = await service.update_todo(mock_session, 1, data)

        assert result.title == "Updated"

    async def test_update_todo_when_not_found(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Raise TodoNotFoundError when the todo does not exist."""
        mock_repository.get_by_id.return_value = None
        data = TodoUpdate(title="Updated")

        with pytest.raises(TodoNotFoundError):
            await service.update_todo(mock_session, 999, data)


class TestDeleteTodo:
    """Tests for TodoService.delete_todo."""

    async def test_delete_todo_when_exists(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Delete the todo when it exists."""
        existing = _make_todo()
        mock_repository.get_by_id.return_value = existing

        await service.delete_todo(mock_session, 1)

        mock_repository.delete.assert_awaited_once_with(mock_session, existing)

    async def test_delete_todo_when_not_found(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Raise TodoNotFoundError when the todo does not exist."""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(TodoNotFoundError):
            await service.delete_todo(mock_session, 999)


class TestCompleteTodo:
    """Tests for TodoService.complete_todo."""

    async def test_complete_todo_when_incomplete(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Mark an incomplete todo as completed."""
        existing = _make_todo(is_completed=False)
        mock_repository.get_by_id.return_value = existing
        completed = _make_todo(is_completed=True)
        mock_repository.update.return_value = completed

        result = await service.complete_todo(mock_session, 1)

        assert result.is_completed is True

    async def test_complete_todo_when_already_completed(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Return the todo unchanged when already completed (idempotent)."""
        existing = _make_todo(is_completed=True)
        mock_repository.get_by_id.return_value = existing

        result = await service.complete_todo(mock_session, 1)

        assert result.is_completed is True
        mock_repository.update.assert_not_awaited()

    async def test_complete_todo_when_not_found(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Raise TodoNotFoundError when the todo does not exist."""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(TodoNotFoundError):
            await service.complete_todo(mock_session, 999)


class TestUncompleteTodo:
    """Tests for TodoService.uncomplete_todo."""

    async def test_uncomplete_todo_when_completed(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Mark a completed todo as incomplete."""
        existing = _make_todo(is_completed=True)
        mock_repository.get_by_id.return_value = existing
        uncompleted = _make_todo(is_completed=False)
        mock_repository.update.return_value = uncompleted

        result = await service.uncomplete_todo(mock_session, 1)

        assert result.is_completed is False

    async def test_uncomplete_todo_when_already_incomplete(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Return the todo unchanged when already incomplete (idempotent)."""
        existing = _make_todo(is_completed=False)
        mock_repository.get_by_id.return_value = existing

        result = await service.uncomplete_todo(mock_session, 1)

        assert result.is_completed is False
        mock_repository.update.assert_not_awaited()

    async def test_uncomplete_todo_when_not_found(
        self,
        service: TodoService,
        mock_repository: MagicMock,
        mock_session: AsyncMock,
    ) -> None:
        """Raise TodoNotFoundError when the todo does not exist."""
        mock_repository.get_by_id.return_value = None

        with pytest.raises(TodoNotFoundError):
            await service.uncomplete_todo(mock_session, 999)
