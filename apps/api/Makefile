format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

check-django:
	uv run python manage.py check

test:
	uv run pytest

check: format-check lint typecheck check-django test