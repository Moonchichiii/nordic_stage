from unittest.mock import MagicMock, patch

from django.test import RequestFactory

from core.utils import generate_unique_slug, get_client_ip


def test_get_client_ip_x_forwarded() -> None:
    factory = RequestFactory()
    request = factory.get("/", HTTP_X_FORWARDED_FOR="192.168.1.1, 10.0.0.1")
    ip = get_client_ip(request)
    assert ip == "192.168.1.1"


def test_get_client_ip_remote_addr() -> None:
    factory = RequestFactory()
    request = factory.get("/", REMOTE_ADDR="127.0.0.1")
    ip = get_client_ip(request)
    assert ip == "127.0.0.1"


@patch("core.utils.Any")
def test_generate_unique_slug_first_try(mock_model: MagicMock) -> None:
    mock_model.objects.filter.return_value.exists.return_value = False

    slug = generate_unique_slug(mock_model, "Hello World")

    assert slug == "hello-world"
    mock_model.objects.filter.assert_called_once_with(slug="hello-world")


@patch("core.utils.Any")
def test_generate_unique_slug_with_collisions(mock_model: MagicMock) -> None:
    mock_model.objects.filter.return_value.exists.side_effect = [
        True,
        True,
        False,
    ]

    slug = generate_unique_slug(mock_model, "Test Event")

    assert slug == "test-event-2"
    assert mock_model.objects.filter.call_count == 3
