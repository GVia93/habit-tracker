from __future__ import annotations

import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import TelegramProfile

User = get_user_model()


class TelegramProfileSerializer(serializers.ModelSerializer):
    """
    CRUD сериализатор для TelegramProfile.
    - user берётся из request.user (клиент руками не присылает)
    - telegram_id уникален, менять его после создания нельзя
    - username хранится без '@'
    """

    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    telegram_id = serializers.IntegerField(validators=[UniqueValidator(queryset=TelegramProfile.objects.all())])

    class Meta:
        model = TelegramProfile
        fields = ("id", "user", "telegram_id", "username", "is_active", "linked_at")
        read_only_fields = ("linked_at",)

    def validate_username(self, value: str) -> str:
        if value and value.startswith("@"):
            value = value[1:]
        if value and not re.fullmatch(r"[A-Za-z0-9_]{1,64}", value):
            raise serializers.ValidationError("Только латиница, цифры и '_' (до 64 символов).")
        return value

    def create(self, validated_data: dict) -> TelegramProfile:
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("Требуется аутентификация для привязки Telegram-профиля.")
        validated_data["user"] = request.user
        return super().create(validated_data)

    def update(self, instance: TelegramProfile, validated_data: dict) -> TelegramProfile:
        if "telegram_id" in validated_data and validated_data["telegram_id"] != instance.telegram_id:
            raise serializers.ValidationError({"telegram_id": "Изменение запрещено."})
        validated_data.pop("user", None)
        return super().update(instance, validated_data)
