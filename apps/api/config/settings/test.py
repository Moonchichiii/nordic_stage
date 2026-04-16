from .base import *  # noqa: F403

DEBUG = False

# Use in-memory DB for fast testing without needing Postgres running
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Execute Celery tasks synchronously in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
