from typing import Any

import pytest

from core.selectors import BaseSelector


def test_base_selector_raises_not_implemented() -> None:
    selector: BaseSelector[Any] = BaseSelector()
    with pytest.raises(NotImplementedError):
        selector.execute()
