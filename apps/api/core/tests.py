import pytest
from core.selectors import BaseSelector

from core.api import custom_exception_handler
from core.exceptions import ApplicationError
from core.models import TimeStampedModel, UUIDModel
from core.services import BaseService


def test_models_are_abstract() -> None:
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True


@pytest.mark.django_db
def test_base_service_raises_not_implemented() -> None:
    """Ensure the base service enforces the execute method."""
    service = BaseService()
    with pytest.raises(NotImplementedError):
        service.process()


def test_base_selector_raises_not_implemented() -> None:
    """Ensure the base selector enforces the get_queryset method."""
    selector = BaseSelector()
    with pytest.raises(NotImplementedError):
        selector.execute()


def test_application_error_initialization() -> None:
    """Ensure the base ApplicationError stores message and extra data."""
    error = ApplicationError("Something went wrong", extra={"code": 123})
    assert error.message == "Something went wrong"
    assert error.extra == {"code": 123}


def test_custom_exception_handler_application_error() -> None:
    """Ensure exception handler formats ApplicationError correctly."""
    error = ApplicationError("Domain failed", extra={"context": "test"})
    response = custom_exception_handler(error, {})

    assert response is not None
    assert response.status_code == 400
    assert response.data["error"] == "ApplicationError"
    assert response.data["message"] == "Domain failed"
