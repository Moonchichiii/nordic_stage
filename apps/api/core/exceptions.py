from typing import Any


class ApplicationError(Exception):
    """
    Base class for all domain-level exceptions in the application.
    """
    def __init__(self, message: str, extra: dict[str, Any] | None = None) -> None:
    def __init__(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.extra = extra or {}


class ResourceNotFoundError(ApplicationError):
    """Raised when a requested resource is not found."""
    pass


class DomainValidationError(ApplicationError):
    """Raised when a business rule validation fails."""
    pass
