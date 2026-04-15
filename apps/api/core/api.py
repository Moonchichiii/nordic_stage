from typing import Any

from core.exceptions import ApplicationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(
    exc: Exception, context: dict[str, Any]
) -> Response | None:
    response = exception_handler(exc, context)

    if isinstance(exc, ApplicationError):
        data = {
            "error": exc.__class__.__name__,
            "message": exc.message,
            "extra": exc.extra,
        }
        return Response(data, status=400)

    return response
