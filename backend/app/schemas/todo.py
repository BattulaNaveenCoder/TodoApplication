"""Pydantic request/response schemas for Todo endpoints."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TodoCreate(BaseModel):
    """Schema for creating a new todo item.

    Attributes:
        title: Todo title, 1-200 characters, whitespace-only rejected.
        description: Optional description, max 1000 characters.
    """

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str) -> str:
        """Reject whitespace-only titles."""
        if not v.strip():
            raise ValueError("Title must not be empty or whitespace only")
        return v.strip()


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item.

    All fields are optional — only provided fields are updated.
    """

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    is_completed: bool | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_whitespace(cls, v: str | None) -> str | None:
        """Reject whitespace-only titles."""
        if v is not None and not v.strip():
            raise ValueError("Title must not be empty or whitespace only")
        return v.strip() if v is not None else v


class TodoResponse(BaseModel):
    """Schema for a single todo item in API responses."""

    id: int
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TodoListResponse(BaseModel):
    """Schema wrapping a list of todos with a count."""

    todos: list[TodoResponse]
    count: int
