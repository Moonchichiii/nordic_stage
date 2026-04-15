import pytest

from core.models import TimeStampedModel, UUIDModel
from core.services import BaseService


def test_models_are_abstract() -> None:
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True

def test_base_service_raises_not_implemented() -> None:
    """Ensure the base service enforces the execute method."""
    service = BaseService()

    with pytest.raises(NotImplementedError):
        service.process()
