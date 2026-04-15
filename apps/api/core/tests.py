from typing import Any

import pytest
import structlog
from django.http import HttpResponse
from django.test import RequestFactory

from core.api import custom_exception_handler
from core.exceptions import ApplicationError
from core.middleware import RequestIDMiddleware, TimingMiddleware
from core.models import TimeStampedModel, UUIDModel
from core.selectors import BaseSelector
from core.services import BaseService


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


def test_request_id_middleware_generates_id() -> None:
    """Ensure RequestIDMiddleware assigns an ID and returns it in headers."""
    factory = RequestFactory()
    request = factory.get("/")

    def get_response(req: Any) -> HttpResponse:
        # Check that the request now has the attribute
        assert hasattr(req, "request_id")
        return HttpResponse("OK")

    middleware = RequestIDMiddleware(get_response)
    response = middleware(request)

    assert "X-Request-ID" in response
    # Use type: ignore to satisfy strict mypy typing on standard WSGIRequest
    assert response["X-Request-ID"] == request.request_id  # type: ignore[attr-defined]


def test_request_id_middleware_uses_existing_id() -> None:
    """Ensure RequestIDMiddleware respects incoming X-Request-ID header."""
    factory = RequestFactory()
    request = factory.get("/", HTTP_X_REQUEST_ID="custom-1234")

    def get_response(req: Any) -> HttpResponse:
        assert req.request_id == "custom-1234"
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
