from typing import Any, Generic, TypeVar

from django.db.models import QuerySet

T = TypeVar("T")


class BaseSelector(Generic[T]):
    """
    Base class for database selectors.
    Encapsulates complex data fetching and filtering logic.
    """

    def get_queryset(self) -> QuerySet[Any]:
        """Return the base queryset for this selector."""
        raise NotImplementedError("Selectors must implement `get_queryset`.")

    def execute(self) -> QuerySet[Any]:
        """
        Execute the selector and return the data.
        Can be overridden if the selector needs to return a single object
        or a formatted dictionary instead of a queryset.
        """
        return self.get_queryset()
