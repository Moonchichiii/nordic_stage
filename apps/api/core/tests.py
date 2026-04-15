import pytest

from core.models import TimeStampedModel, UUIDModel
from core.selectors import BaseSelector


def test_models_are_abstract() -> None:
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True

def test_base_selector_raises_not_implemented() -> None:
    """Ensure the base selector enforces the get_queryset method."""
    selector = BaseSelector()

    with pytest.raises(NotImplementedError):
        selector.execute()
