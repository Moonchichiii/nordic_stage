from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from django.test import RequestFactory

from core.api import custom_exception_handler
from core.exceptions import ApplicationError
from core.models import TimeStampedModel, UUIDModel
from core.selectors import BaseSelector
from core.services import BaseService
from core.utils import generate_unique_slug, get_client_ip


def test_models_are_abstract() -> None:
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True


def test_base_selector_raises_not_implemented() -> None:
    """Ensure the base selector enforces the get_queryset method."""
    selector: BaseSelector[Any] = BaseSelector()

    with pytest.raises(NotImplementedError):
        selector.execute()


def test_base_service_raises_not_implemented() -> None:
    """Ensure the base service enforces the execute method."""
    service = BaseService()
    with pytest.raises(NotImplementedError):
        # Call execute directly to avoid triggering @transaction.atomic
        # on process()
        service.execute()


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


def test_get_client_ip_x_forwarded() -> None:
    """Ensure we get the first IP from X-Forwarded-For if present."""
    factory = RequestFactory()
    # HTTP_ headers in RequestFactory map to HTTP_ prefix in META
    request = factory.get("/", HTTP_X_FORWARDED_FOR="192.168.1.1, 10.0.0.1")
    ip = get_client_ip(request)
    assert ip == "192.168.1.1"


def test_get_client_ip_remote_addr() -> None:
    """Ensure we fall back to REMOTE_ADDR if no forwarded header."""
    factory = RequestFactory()
    request = factory.get("/", REMOTE_ADDR="127.0.0.1")
    ip = get_client_ip(request)
    assert ip == "127.0.0.1"


@patch("core.utils.Any")
def test_generate_unique_slug_first_try(mock_model: MagicMock) -> None:
    """Ensure we get the base slug if it doesn't exist."""
    mock_model.objects.filter.return_value.exists.return_value = False

    slug = generate_unique_slug(mock_model, "Hello World")

    assert slug == "hello-world"
    mock_model.objects.filter.assert_called_once_with(slug="hello-world")


@patch("core.utils.Any")
def test_generate_unique_slug_with_collisions(mock_model: MagicMock) -> None:
    """Ensure we append a counter if collisions occur."""
    mock_model.objects.filter.return_value.exists.side_effect = [
        True,
        True,
        False,
    ]

    slug = generate_unique_slug(mock_model, "Test Event")

    assert slug == "test-event-2"
    assert mock_model.objects.filter.call_count == 3
