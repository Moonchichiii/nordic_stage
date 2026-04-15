import time
import uuid
from typing import Callable

import structlog
from django.http import HttpRequest, HttpResponse

logger = structlog.get_logger(__name__)


class RequestIDMiddleware:
    """
    Ensures every request has a unique ID for distributed tracing.
    Binds the request ID to the structured logger.
    """
    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Get from load balancer/proxy, or generate a new one
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.request_id = request_id  # type: ignore

        # Bind the request ID to all logs generated during this request
        with structlog.contextvars.bound_contextvars(request_id=request_id):
            response = self.get_response(request)

        # Return the ID to the client
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
