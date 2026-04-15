from typing import Any

from django.db import transaction


class BaseService:
    """
    Base class for all business logic services.
    Encapsulates complex logic to keep models and views thin.
    """

    def __init__(self, user: Any | None = None) -> None:
        self.user = user

    def pre_execute(self) -> None:
        """Hook for validation or setup before execution."""
        pass

    def execute(self) -> Any:
        """Main business logic implementation."""
        raise NotImplementedError(
            "Services must implement the `execute` method."
        )

    def post_execute(self, result: Any) -> None:
        """Hook for side effects (e.g., sending emails) after execution."""
        pass

    @transaction.atomic
    def process(self) -> Any:
        """
        Runs the service lifecycle within a database transaction.
        """
        self.pre_execute()
        result = self.execute()
        self.post_execute(result)
        return result
