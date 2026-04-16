from core.models import TimeStampedModel, UUIDModel


def test_models_are_abstract() -> None:
    assert UUIDModel._meta.abstract is True
    assert TimeStampedModel._meta.abstract is True
