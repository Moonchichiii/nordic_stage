from core.exceptions import ApplicationError
from core.models import TimeStampedModel, UUIDModel


def test_models_are_abstract() -> None:
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True


def test_application_error_initialization() -> None:
    """Ensure the base ApplicationError stores message and extra data."""
    error = ApplicationError("Something went wrong", extra={"code": 123})
    
    assert error.message == "Something went wrong"
    assert error.extra == {"code": 123}
