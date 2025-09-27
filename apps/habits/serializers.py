from __future__ import annotations

from rest_framework import serializers

from .models import Habit
from .validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки с комплексной валидацией."""

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "action",
            "place",
            "time",
            "is_pleasant",
            "related_habit",
            "reward",
            "duration_seconds",
            "periodicity",
            "is_public",
            "created_at",
        )
        read_only_fields = ("user", "created_at")

    def validate(self, attrs: dict) -> dict:
        # Собираем полную картину при partial update
        data = {**getattr(self, "initial_data", {}), **attrs}
        if self.instance:
            data.setdefault("is_pleasant", self.instance.is_pleasant)
            data.setdefault("related_habit", attrs.get("related_habit", self.instance.related_habit))
        return validate_habit(data)

    def create(self, validated_data: dict) -> Habit:
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
