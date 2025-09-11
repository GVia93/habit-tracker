import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_success(api_client, create_user):
    """
    Тест успешного логина.

    Действия:
    - создаём пользователя в БД;
    - отправляем POST-запрос на эндпоинт `auth-login` с корректными email и паролем;
    - проверяем, что вернулся статус 200 и в ответе есть токены доступа и обновления.
    """
    user = create_user(email="u@example.com", password="password123")
    url = reverse("users:auth-login")

    resp = api_client.post(url, {"email": user.email, "password": "password123"}, format="json")

    assert resp.status_code == 200
    assert "access" in resp.json()
    assert "refresh" in resp.json()


@pytest.mark.django_db
def test_login_failure(api_client, create_user):
    """
    Тест неуспешного логина с неверным паролем.

    Действия:
    - создаём пользователя в БД;
    - отправляем POST-запрос на эндпоинт `auth-login` с неправильным паролем;
    - проверяем, что вернулся статус 401 и сообщение об ошибке.
    """
    user = create_user(email="u@example.com", password="password123")
    url = reverse("users:auth-login")

    resp = api_client.post(url, {"email": user.email, "password": "wrong"}, format="json")

    assert resp.status_code == 401
    assert "detail" in resp.json()
