"""SQLAlchemy model for the Todo entity."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Todo(Base):
    """Todo item database model.

    Attributes:
        id: Primary key, auto-incremented.
        title: Todo title, max 200 characters.
        description: Optional description, max 1000 characters.
        is_completed: Completion status, defaults to False.
        created_at: Timestamp of creation, set by server.
        updated_at: Timestamp of last update, auto-updated.
    """

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
