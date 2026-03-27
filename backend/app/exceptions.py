"""Custom domain exceptions for the application."""


class AppException(Exception):
    """Base exception for all application domain errors.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code to return.
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class TodoNotFoundError(AppException):
    """Raised when a requested todo item does not exist."""

    def __init__(self, todo_id: int) -> None:
        super().__init__(
            message=f"Todo with id {todo_id} not found",
            status_code=404,
        )


class ValidationError(AppException):
    """Raised when input data fails business validation."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=422)
