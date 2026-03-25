"""Business logic layer for Todo operations."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import TodoNotFoundError
from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoService:
    """Service handling all Todo business logic.

    Delegates data access to TodoRepository and raises domain
    exceptions when business rules are violated.
    """

    def __init__(self, repository: TodoRepository) -> None:
        self._repository = repository

    async def get_todo(self, session: AsyncSession, todo_id: int) -> Todo:
        """Retrieve a single todo by ID.

        Args:
            session: The async database session.
            todo_id: The ID of the todo to retrieve.

        Returns:
            The Todo instance.

        Raises:
            TodoNotFoundError: If no todo exists with the given ID.
        """
        todo = await self._repository.get_by_id(session, todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        return todo

    async def list_todos(self, session: AsyncSession) -> list[Todo]:
        """Retrieve all todos ordered by creation date descending.

        Args:
            session: The async database session.

        Returns:
            A list of all Todo instances.
        """
        return await self._repository.get_all(session)

    async def create_todo(self, session: AsyncSession, data: TodoCreate) -> Todo:
        """Create a new todo item.

        Args:
            session: The async database session.
            data: Validated todo creation data.

        Returns:
            The newly created Todo instance.
        """
        return await self._repository.create(session, data)

    async def update_todo(
        self, session: AsyncSession, todo_id: int, data: TodoUpdate
    ) -> Todo:
        """Update an existing todo item.

        Args:
            session: The async database session.
            todo_id: The ID of the todo to update.
            data: Validated update data.

        Returns:
            The updated Todo instance.

        Raises:
            TodoNotFoundError: If no todo exists with the given ID.
        """
        todo = await self._repository.get_by_id(session, todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        return await self._repository.update(session, todo, data)

    async def delete_todo(self, session: AsyncSession, todo_id: int) -> None:
        """Delete a todo item.

        Args:
            session: The async database session.
            todo_id: The ID of the todo to delete.

        Raises:
            TodoNotFoundError: If no todo exists with the given ID.
        """
        todo = await self._repository.get_by_id(session, todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        await self._repository.delete(session, todo)

    async def complete_todo(self, session: AsyncSession, todo_id: int) -> Todo:
        """Mark a todo as completed (idempotent).

        Args:
            session: The async database session.
            todo_id: The ID of the todo to complete.

        Returns:
            The updated Todo instance.

        Raises:
            TodoNotFoundError: If no todo exists with the given ID.
        """
        todo = await self._repository.get_by_id(session, todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        if todo.is_completed:
            return todo
        return await self._repository.update(
            session, todo, TodoUpdate(is_completed=True)
        )

    async def uncomplete_todo(self, session: AsyncSession, todo_id: int) -> Todo:
        """Mark a todo as incomplete (idempotent).

        Args:
            session: The async database session.
            todo_id: The ID of the todo to uncomplete.

        Returns:
            The updated Todo instance.

        Raises:
            TodoNotFoundError: If no todo exists with the given ID.
        """
        todo = await self._repository.get_by_id(session, todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        if not todo.is_completed:
            return todo
        return await self._repository.update(
            session, todo, TodoUpdate(is_completed=False)
        )
