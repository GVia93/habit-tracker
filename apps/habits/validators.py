from __future__ import annotations

from rest_framework import serializers


def validate_habit(data: dict) -> dict:
    """Бизнес-валидаторы из ТЗ."""
    is_pleasant = data.get("is_pleasant")
    reward = data.get("reward")
    related = data.get("related_habit")
    duration = data.get("duration_seconds")
    periodicity = data.get("periodicity")

    if duration is not None and duration > 120:
        raise serializers.ValidationError({"duration_seconds": "Длительность не более 120 секунд."})
    if periodicity is not None and (periodicity < 1 or periodicity > 7):
        raise serializers.ValidationError({"periodicity": "Периодичность от 1 до 7 дней."})

    if reward and related:
        raise serializers.ValidationError("Укажите либо reward, либо related_habit, но не оба.")

    if is_pleasant:
        if reward or related:
            raise serializers.ValidationError("Для приятной привычки нельзя указывать reward/related_habit.")
    else:
        if related is not None and not related.is_pleasant:
            raise serializers.ValidationError({"related_habit": "Можно ссылаться только на приятную привычку."})

    return data
