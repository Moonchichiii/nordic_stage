import pytest

from core.services import BaseService


def test_base_service_raises_not_implemented() -> None:
    service = BaseService()
    with pytest.raises(NotImplementedError):
        service.execute()
