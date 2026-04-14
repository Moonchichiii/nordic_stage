.PHONY: install dev-api dev-web

# ==============================================================================
# Setup & Installation
# ==============================================================================
install:
@echo "Installing frontend dependencies..."
bun install
@echo "Installing backend dependencies..."
cd apps/api && uv pip install -e ".[dev]"

# ==============================================================================
# Development Servers
# ==============================================================================
dev-api:
cd apps/api && uv run python manage.py runserver

dev-web:
cd apps/web && bun run dev
