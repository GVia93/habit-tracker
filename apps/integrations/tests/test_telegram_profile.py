import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.integrations.models import TelegramProfile

User = get_user_model()


@pytest.mark.django_db
def test_create_telegram_profile_model():
    """
    Базовый тест модели: создание напрямую через ORM.
    """
    u = User.objects.create_user(email="tg@x.com", password="password123")
    tp = TelegramProfile.objects.create(user=u, telegram_id=123456)
    assert tp.user_id == u.id
    assert tp.telegram_id == 123456


@pytest.mark.django_db
def test_api_create_telegram_profile(api_client, create_user):
    """
    Тест API: создание TelegramProfile через POST /integrations/telegram-profiles/.
    """
    user = create_user(email="api@tg.com")
    api_client.force_authenticate(user=user)

    url = reverse("integrations:telegram-profile-list")
    payload = {"telegram_id": 999999, "username": "tester"}
    resp = api_client.post(url, payload, format="json")

    assert resp.status_code == 201
    data = resp.json()
    assert data["telegram_id"] == 999999
    assert data["username"] == "tester"
    assert data["user"] == user.email


@pytest.mark.django_db
def test_api_update_disallow_telegram_id(api_client, create_user):
    """
    Тест API: нельзя изменить telegram_id после создания.
    """
    user = create_user(email="edit@tg.com")
    profile = TelegramProfile.objects.create(user=user, telegram_id=111111)
    api_client.force_authenticate(user=user)

    url = reverse("integrations:telegram-profile-detail", args=[profile.id])
    resp = api_client.patch(url, {"telegram_id": 222222}, format="json")

    assert resp.status_code == 400
    assert "telegram_id" in resp.json()


@pytest.mark.django_db
def test_api_list_only_own_profile(api_client, create_user):
    """
    Тест API: пользователь видит только свой TelegramProfile.
    """
    user1 = create_user(email="u1@tg.com")
    user2 = create_user(email="u2@tg.com")

    TelegramProfile.objects.create(user=user1, telegram_id=111111)
    TelegramProfile.objects.create(user=user2, telegram_id=222222)

    api_client.force_authenticate(user=user1)
    url = reverse("integrations:telegram-profile-list")
    resp = api_client.get(url)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["user"] == user1.email
