import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_success(api_client):
    """
    Тест успешной регистрации нового пользователя.

    Действия:
    - отправляем POST-запрос на эндпоинт `auth-register`
      с корректным email и валидным паролем;
    - проверяем, что вернулся статус 201 (создано);
    - убеждаемся, что email в ответе совпадает с переданным.
    """
    r = api_client.post(
        reverse("users:auth-register"),
        {"email": "u@example.com", "password": "password123"},
        format="json",
    )
    assert r.status_code == 201
    assert r.data["email"] == "u@example.com"


@pytest.mark.django_db
def test_register_password_too_short(api_client):
    """
    Тест неуспешной регистрации при слишком коротком пароле.

    Действия:
    - отправляем POST-запрос на эндпоинт `auth-register`
      с корректным email, но слишком коротким паролем;
    - проверяем, что вернулся статус 400 (ошибка валидации).
    """
    r = api_client.post(
        reverse("users:auth-register"),
        {"email": "a@a.com", "password": "short"},
        format="json",
    )
    assert r.status_code == 400
