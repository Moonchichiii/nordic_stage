from core.api import custom_exception_handler
from core.exceptions import ApplicationError


def test_application_error_initialization() -> None:
    error = ApplicationError("Something went wrong", extra={"code": 123})
    assert error.message == "Something went wrong"
    assert error.extra == {"code": 123}


def test_custom_exception_handler_application_error() -> None:
    error = ApplicationError("Domain failed", extra={"context": "test"})
    response = custom_exception_handler(error, {})

    assert response is not None
    assert response.status_code == 400
    assert response.data["error"] == "ApplicationError"
    assert response.data["message"] == "Domain failed"
