import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_refresh_success(api_client, create_user):
    """
    Тест успешного обновления access-токена.

    Действия:
    - создаём пользователя в БД;
    - выполняем логин, получаем refresh-токен;
    - отправляем POST-запрос на эндпоинт `auth-refresh` с refresh-токеном;
    - проверяем, что вернулся новый access-токен.
    """
    user = create_user(email="u2@example.com", password="password123")
    login_url = reverse("users:auth-login")

    login_resp = api_client.post(login_url, {"email": user.email, "password": "password123"}, format="json")
    refresh = login_resp.json()["refresh"]

    refresh_url = reverse("users:auth-refresh")
    refresh_resp = api_client.post(refresh_url, {"refresh": refresh}, format="json")

    assert refresh_resp.status_code == 200
    assert "access" in refresh_resp.json()
