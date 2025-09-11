import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """DRF APIClient для тестов."""
    return APIClient()


@pytest.fixture
def create_user(db):
    """
    Фабрика для создания пользователей.
    Пример:
        user = create_user(email="u@example.com", password="123")
    """

    def make_user(**kwargs):
        defaults = {"email": "test@example.com", "password": "password123"}
        defaults.update(kwargs)
        user = User.objects.create_user(
            email=defaults["email"],
            password=defaults["password"],
        )
        return user

    return make_user
