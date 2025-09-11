from __future__ import annotations

from django.conf import settings
from django.db import models


class Habit(models.Model):
    """Модель привычки с периодичностью и флагом публичности."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField(help_text="Локальное время выполнения")
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration_seconds = models.PositiveSmallIntegerField(default=60, help_text="Длительность ≤ 120 секунд")
    periodicity = models.PositiveSmallIntegerField(default=1, help_text="через каждые N дней (1..7)")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.action} @ {self.time} in {self.place}"
