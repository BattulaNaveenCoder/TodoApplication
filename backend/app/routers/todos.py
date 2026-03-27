"""API routes for Todo resource."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories.todo_repository import TodoRepository
from app.schemas.todo import TodoCreate, TodoListResponse, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])


def get_todo_service() -> TodoService:
    """Create and return a TodoService instance with its repository."""
    return TodoService(repository=TodoRepository())


@router.get(
    "",
    response_model=TodoListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_todos(
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> TodoListResponse:
    """List all todo items ordered by creation date descending.

    Returns:
        A TodoListResponse containing all todos and count.
    """
    todos = await service.list_todos(session)
    items = [TodoResponse.model_validate(t) for t in todos]
    return TodoListResponse(todos=items, count=len(items))


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    data: TodoCreate,
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Create a new todo item.

    Args:
        data: Validated todo creation payload.

    Returns:
        The newly created todo.
    """
    todo = await service.create_todo(session, data)
    return TodoResponse.model_validate(todo)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
async def get_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Get a single todo by ID.

    Args:
        todo_id: The ID of the todo to retrieve.

    Returns:
        The requested todo.

    Raises:
        TodoNotFoundError: 404 if todo not found.
    """
    todo = await service.get_todo(session, todo_id)
    return TodoResponse.model_validate(todo)


@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
async def update_todo(
    todo_id: int,
    data: TodoUpdate,
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Update an existing todo item.

    Args:
        todo_id: The ID of the todo to update.
        data: Validated update payload.

    Returns:
        The updated todo.

    Raises:
        TodoNotFoundError: 404 if todo not found.
    """
    todo = await service.update_todo(session, todo_id, data)
    return TodoResponse.model_validate(todo)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> Response:
    """Delete a todo item.

    Args:
        todo_id: The ID of the todo to delete.

    Raises:
        TodoNotFoundError: 404 if todo not found.
    """
    await service.delete_todo(session, todo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{todo_id}/complete",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
async def complete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Mark a todo as completed.

    Args:
        todo_id: The ID of the todo to mark complete.

    Returns:
        The updated todo.

    Raises:
        TodoNotFoundError: 404 if todo not found.
    """
    todo = await service.complete_todo(session, todo_id)
    return TodoResponse.model_validate(todo)


@router.patch(
    "/{todo_id}/uncomplete",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
async def uncomplete_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_db),
    service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Mark a todo as incomplete.

    Args:
        todo_id: The ID of the todo to mark incomplete.

    Returns:
        The updated todo.

    Raises:
        TodoNotFoundError: 404 if todo not found.
    """
    todo = await service.uncomplete_todo(session, todo_id)
    return TodoResponse.model_validate(todo)
