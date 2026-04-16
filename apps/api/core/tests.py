from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import structlog
from django.http import HttpResponse
from django.test import RequestFactory

from core.api import custom_exception_handler
from core.exceptions import ApplicationError
from core.middleware import CSPMiddleware, RequestIDMiddleware, TimingMiddleware
from core.models import TimeStampedModel, UUIDModel
from core.selectors import BaseSelector
from core.services import BaseService
from core.tasks import BaseTask, debug_task, send_email_task
from core.utils import generate_unique_slug, get_client_ip


# Models Tests
def test_models_are_abstract() -> None:
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True


# Base Classes Tests
def test_base_selector_raises_not_implemented() -> None:
    """Ensure the base selector enforces the get_queryset method."""
    selector: BaseSelector[Any] = BaseSelector()
    with pytest.raises(NotImplementedError):
        selector.execute()


def test_base_service_raises_not_implemented() -> None:
    """Ensure the base service enforces the execute method."""
    service = BaseService()
    with pytest.raises(NotImplementedError):
        service.execute()


# Exception Tests
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


# Middleware Tests
def test_request_id_middleware_generates_id() -> None:
    """Ensure RequestIDMiddleware assigns an ID and returns it in headers."""
    factory = RequestFactory()
    request = factory.get("/")

    def get_response(req: Any) -> HttpResponse:
        assert hasattr(req, "request_id")
        return HttpResponse("OK")

    middleware = RequestIDMiddleware(get_response)
    response = middleware(request)

    assert "X-Request-ID" in response
    assert response["X-Request-ID"] == getattr(request, "request_id", None)


def test_request_id_middleware_uses_existing_id() -> None:
    """Ensure RequestIDMiddleware respects incoming X-Request-ID header."""
    factory = RequestFactory()
    request = factory.get("/", HTTP_X_REQUEST_ID="custom-1234")

    def get_response(req: Any) -> HttpResponse:
        assert getattr(req, "request_id", None) == "custom-1234"
        return HttpResponse("OK")

    middleware = RequestIDMiddleware(get_response)
    response = middleware(request)

    assert response["X-Request-ID"] == "custom-1234"


def test_timing_middleware_logs_duration() -> None:
    """Ensure TimingMiddleware calculates duration and logs it."""
    factory = RequestFactory()
    request = factory.get("/test-path/")

    def get_response(req: Any) -> HttpResponse:
        return HttpResponse("OK")

    middleware = TimingMiddleware(get_response)

    with structlog.testing.capture_logs() as cap_logs:
        response = middleware(request)

    assert response.status_code == 200
    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "request_finished"
    assert cap_logs[0]["path"] == "/test-path/"
    assert "duration_s" in cap_logs[0]


def test_csp_middleware_sets_header() -> None:
    """Ensure custom CSPMiddleware applies the CSP header."""
    factory = RequestFactory()
    request = factory.get("/")

    def get_response(req: Any) -> HttpResponse:
        return HttpResponse("OK")

    middleware = CSPMiddleware(get_response)
    response = middleware(request)

    assert "Content-Security-Policy" in response
    assert "default-src 'self'" in response["Content-Security-Policy"]


# Utility Tests
def test_get_client_ip_x_forwarded() -> None:
    """Ensure we get the first IP from X-Forwarded-For if present."""
    factory = RequestFactory()
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


# Task Tests
def test_debug_task() -> None:
    """Ensure debug task runs and returns pong."""
    assert debug_task() == "pong"


def test_send_email_task() -> None:
    """Ensure the placeholder email task works properly."""
    result = send_email_task("test@example.com", "Hello", "This is a test body")
    assert result is True


def test_basetask_on_failure() -> None:
    """Ensure the BaseTask logs errors appropriately on failure."""
    task = BaseTask()
    task.name = "test_task"

    with structlog.testing.capture_logs() as cap_logs:
        task.on_failure(Exception("Test error"), "123", (), {}, None)

    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "task_failed"
    assert cap_logs[0]["task_name"] == "test_task"


def test_basetask_on_success() -> None:
    """Ensure the BaseTask logs successes appropriately."""
    task = BaseTask()
    task.name = "test_task"

    with structlog.testing.capture_logs() as cap_logs:
        task.on_success("retval", "123", (), {})

    assert len(cap_logs) == 1
    assert cap_logs[0]["event"] == "task_succeeded"
    assert cap_logs[0]["task_name"] == "test_task"
