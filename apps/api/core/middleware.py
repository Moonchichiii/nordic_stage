import time
from typing import Callable

import structlog
from django.http import HttpRequest, HttpResponse

logger = structlog.get_logger(__name__)


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
            duration_s=round(duration, 4)
        )

        return response
