from typing import Any

import structlog
from django.http import HttpResponse
from django.test import RequestFactory

from core.middleware import CSPMiddleware, RequestIDMiddleware, TimingMiddleware


def test_request_id_middleware_generates_id() -> None:
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
    factory = RequestFactory()
    request = factory.get("/", HTTP_X_REQUEST_ID="custom-1234")

    def get_response(req: Any) -> HttpResponse:
        assert getattr(req, "request_id", None) == "custom-1234"
        return HttpResponse("OK")

    middleware = RequestIDMiddleware(get_response)
    response = middleware(request)

    assert response["X-Request-ID"] == "custom-1234"


def test_timing_middleware_logs_duration() -> None:
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
    factory = RequestFactory()
    request = factory.get("/")

    def get_response(req: Any) -> HttpResponse:
        return HttpResponse("OK")

    middleware = CSPMiddleware(get_response)
    response = middleware(request)

    assert "Content-Security-Policy" in response
    assert "default-src 'self'" in response["Content-Security-Policy"]
