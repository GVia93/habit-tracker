from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя (пароль ≥ 8, email обязателен)."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "username")

    def create(self, validated_data: dict) -> User:
        password = validated_data.pop("password")
        validated_data["username"] = (validated_data.get("username") or "").strip()
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
