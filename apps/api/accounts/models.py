from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseDomainModel, TimeStampedModel, UUIDModel


class User(AbstractUser, UUIDModel, TimeStampedModel):
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.username


class Profile(BaseDomainModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    display_name = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.display_name or self.user.username
