# Docker Infrastructure Runbook

This guide covers the local containerized environment for Nordic Stage.

## Architecture

We use `docker-compose` to orchestrate:

- **db**: PostgreSQL 16
- **redis**: Redis 7
- **api**: Django backend (runs via Gunicorn)
- **web**: Next.js frontend (standalone build)
- **nginx**: Reverse proxy mapping port 80 to the web and api services

## Common Commands

All commands should be run from the root of the repository.

### Start the stack in the background

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

### Rebuild after adding new dependencies

If you add new pip/uv packages or node/bun modules:

```bash
docker compose -f infra/docker/docker-compose.yml build
# or to start right away:
docker compose -f infra/docker/docker-compose.yml up -d --build
```

### View logs

Follow logs for all services:

```bash
docker compose -f infra/docker/docker-compose.yml logs -f
```

Tail logs for a specific service (e.g., api):

```bash
docker compose -f infra/docker/docker-compose.yml logs -f api
```

### Run Django management commands

To run commands inside the running API container:

```bash
docker compose -f infra/docker/docker-compose.yml exec api python manage.py migrate
docker compose -f infra/docker/docker-compose.yml exec api python manage.py createsuperuser
```

### Shutting down

Stop the containers but preserve the database volume:

```bash
docker compose -f infra/docker/docker-compose.yml down
```

Stop the containers AND wipe the database (complete reset):

```bash
docker compose -f infra/docker/docker-compose.yml down -v
```