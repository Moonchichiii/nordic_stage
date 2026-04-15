from .base import *  # noqa: F403

DEBUG = False

# Use in-memory DB for fast testing without needing Postgres running
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
