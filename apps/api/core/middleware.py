import time
import uuid
from typing import Callable

import structlog
from django.conf import settings
from django.http import HttpRequest, HttpResponse

logger = structlog.get_logger(__name__)

class RequestIDMiddleware:
    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id  # type: ignore

        with structlog.contextvars.bound_contextvars(request_id=request_id):
            response = self.get_response(request)

        response["X-Request-ID"] = request_id
        return response


class TimingMiddleware:
    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        logger.info(
            "request_finished",
            method=request.method,
            path=request.path,
            status=response.status_code,
            duration_s=round(duration, 4),
        )

        return response


class CSPMiddleware:
    """
    Injects the Content-Security-Policy header into every response.
    """
    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        csp = getattr(
            settings,
            "SECURE_CONTENT_SECURITY_POLICY",
            "default-src 'self'; frame-ancestors 'none';"
        )

        if "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = csp

        return response
