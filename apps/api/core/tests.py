import pytest
from core.models import TimeStampedModel, UUIDModel
from django.db import models


def test_models_are_abstract():
    """Ensure our base domain models remain abstract."""
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True
