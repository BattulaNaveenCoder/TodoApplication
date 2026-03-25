"""Unit tests for TodoService with mocked repository."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.exceptions import TodoNotFoundError
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services.todo_service import TodoService


@pytest.fixture()
def mock_repo() -> AsyncMock:
    """Return a mock TodoRepository."""
    return AsyncMock()


@pytest.fixture()
def service(mock_repo: AsyncMock) -> TodoService:
    """Return a TodoService with a mocked repository."""
    return TodoService(repository=mock_repo)


@pytest.fixture()
def mock_session() -> AsyncMock:
    """Return a mock AsyncSession."""
    return AsyncMock()


@pytest.fixture()
def mock_todo() -> MagicMock:
    """Return a mock Todo instance."""
    todo = MagicMock(spec=Todo)
    todo.id = 1
    todo.title = "Test Todo"
    todo.description = "Test description"
    todo.is_completed = False
    return todo


async def test_get_todo_when_exists_returns_todo(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock, mock_todo: MagicMock
) -> None:
    """Verify get_todo returns the todo when the repo finds it."""
    mock_repo.get_by_id.return_value = mock_todo
    result = await service.get_todo(mock_session, 1)
    assert result == mock_todo
    mock_repo.get_by_id.assert_called_once_with(mock_session, 1)


async def test_get_todo_when_not_found_raises_todo_not_found_error(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock
) -> None:
    """Verify get_todo raises TodoNotFoundError when repo returns None."""
    mock_repo.get_by_id.return_value = None
    with pytest.raises(TodoNotFoundError):
        await service.get_todo(mock_session, 999)


async def test_create_todo_when_valid_returns_todo(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock, mock_todo: MagicMock
) -> None:
    """Verify create_todo delegates to the repository and returns result."""
    mock_repo.create.return_value = mock_todo
    data = TodoCreate(title="New Todo")
    result = await service.create_todo(mock_session, data)
    assert result == mock_todo
    mock_repo.create.assert_called_once_with(mock_session, data)


async def test_update_todo_when_not_found_raises_error(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock
) -> None:
    """Verify update_todo raises TodoNotFoundError when todo missing."""
    mock_repo.get_by_id.return_value = None
    data = TodoUpdate(title="Updated")
    with pytest.raises(TodoNotFoundError):
        await service.update_todo(mock_session, 999, data)


async def test_complete_todo_sets_is_completed_true(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock, mock_todo: MagicMock
) -> None:
    """Verify complete_todo marks the todo as completed."""
    mock_todo.is_completed = False
    mock_repo.get_by_id.return_value = mock_todo
    completed_todo = MagicMock(spec=Todo)
    completed_todo.is_completed = True
    mock_repo.update.return_value = completed_todo
    result = await service.complete_todo(mock_session, 1)
    assert result.is_completed is True


async def test_uncomplete_todo_sets_is_completed_false(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock, mock_todo: MagicMock
) -> None:
    """Verify uncomplete_todo marks the todo as incomplete."""
    mock_todo.is_completed = True
    mock_repo.get_by_id.return_value = mock_todo
    uncompleted_todo = MagicMock(spec=Todo)
    uncompleted_todo.is_completed = False
    mock_repo.update.return_value = uncompleted_todo
    result = await service.uncomplete_todo(mock_session, 1)
    assert result.is_completed is False


async def test_delete_todo_when_not_found_raises_error(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock
) -> None:
    """Verify delete_todo raises TodoNotFoundError when todo missing."""
    mock_repo.get_by_id.return_value = None
    with pytest.raises(TodoNotFoundError):
        await service.delete_todo(mock_session, 999)


async def test_complete_todo_when_already_completed_remains_completed(
    service: TodoService, mock_repo: AsyncMock, mock_session: AsyncMock, mock_todo: MagicMock
) -> None:
    """Verify complete_todo is idempotent — already completed todo stays as is."""
    mock_todo.is_completed = True
    mock_repo.get_by_id.return_value = mock_todo
    result = await service.complete_todo(mock_session, 1)
    assert result == mock_todo
    mock_repo.update.assert_not_called()
