from __future__ import annotations

from django.conf import settings
from django.db import models


class TelegramProfile(models.Model):
    """Привязка Telegram ↔ User для рассылки напоминаний."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="telegram_profile")
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    linked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Telegram профиль"
        verbose_name_plural = "Telegram профили"
        ordering = ["-linked_at"]

    def __str__(self) -> str:
        return f"{self.user.email} ↔ {self.telegram_id}"
