"""Data access layer for Todo entities."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


class TodoRepository:
    """Repository for Todo CRUD operations.

    All methods are async and accept an AsyncSession.
    Returns model instances or None — never raises HTTP exceptions.
    """

    async def get_by_id(self, session: AsyncSession, todo_id: int) -> Todo | None:
        """Fetch a single todo by its primary key.

        Args:
            session: The async database session.
            todo_id: The ID of the todo to retrieve.

        Returns:
            The Todo instance if found, otherwise None.
        """
        result = await session.execute(select(Todo).where(Todo.id == todo_id))
        return result.scalar_one_or_none()

    async def get_all(self, session: AsyncSession) -> list[Todo]:
        """Fetch all todo items ordered by creation date descending.

        Args:
            session: The async database session.

        Returns:
            A list of all Todo instances.
        """
        result = await session.execute(select(Todo).order_by(Todo.created_at.desc()))
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, data: TodoCreate) -> Todo:
        """Create a new todo item.

        Args:
            session: The async database session.
            data: Validated todo creation data.

        Returns:
            The newly created Todo instance.
        """
        todo = Todo(
            title=data.title,
            description=data.description,
        )
        session.add(todo)
        await session.flush()
        await session.refresh(todo)
        return todo

    async def update(
        self, session: AsyncSession, todo: Todo, data: TodoUpdate
    ) -> Todo:
        """Update an existing todo item with provided fields.

        Args:
            session: The async database session.
            todo: The existing Todo instance to update.
            data: Validated update data; only non-None fields are applied.

        Returns:
            The updated Todo instance.
        """
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)
        await session.flush()
        await session.refresh(todo)
        return todo

    async def delete(self, session: AsyncSession, todo: Todo) -> None:
        """Delete a todo item from the database.

        Args:
            session: The async database session.
            todo: The Todo instance to delete.
        """
        await session.delete(todo)
        await session.flush()
