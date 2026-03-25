"""Custom domain exceptions for the application."""


class AppException(Exception):
    """Base exception for all application domain errors.

    Attributes:
        message: Human-readable error description.
        code: Machine-readable error code.
    """

    def __init__(self, message: str, code: str = "APP_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class TodoNotFoundError(AppException):
    """Raised when a requested todo item does not exist."""

    def __init__(self, todo_id: int) -> None:
        super().__init__(
            message=f"Todo with id {todo_id} not found",
            code="TODO_NOT_FOUND",
        )


class ValidationError(AppException):
    """Raised when input data fails business validation."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="VALIDATION_ERROR")
