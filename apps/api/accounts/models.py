from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel, UUIDModel


class User(AbstractUser, UUIDModel, TimeStampedModel):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.username
