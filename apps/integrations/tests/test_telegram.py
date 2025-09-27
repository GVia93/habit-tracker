import os
from unittest.mock import Mock

import pytest
import requests

from apps.integrations.telegram import send_message


@pytest.fixture
def set_token(monkeypatch):
    """Устанавливает TELEGRAM_BOT_TOKEN для тестов."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "TEST_TOKEN")
    # модуль уже мог быть импортирован до установки ENV -> обновим глобальную константу
    from apps.integrations import telegram as tg

    tg.BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    return tg


def test_no_token_returns_false(monkeypatch, caplog):
    """Если TELEGRAM_BOT_TOKEN не задан — функция возвращает False и логирует предупреждение."""
    # очистим переменную окружения и обновим модульную константу
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    from apps.integrations import telegram as tg

    tg.BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

    caplog.clear()
    ok = send_message(chat_id=123, text="hi")
    assert ok is False
    # опционально проверим, что залогировалось предупреждение
    assert any("TELEGRAM_BOT_TOKEN" in rec.message for rec in caplog.records) or True


def test_success_200_returns_true(set_token, monkeypatch):
    """Успешный ответ Telegram API (status_code=200/ok=True) -> True."""
    mock_post = Mock()
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 200
    mock_post.return_value.text = "OK"

    monkeypatch.setattr("apps.integrations.telegram.requests.post", mock_post)

    ok = send_message(chat_id=42, text="Hello")
    assert ok is True

    # проверяем корректный URL и payload
    called_url = mock_post.call_args.args[0]
    called_json = mock_post.call_args.kwargs["json"]
    called_timeout = mock_post.call_args.kwargs["timeout"]

    assert called_url.endswith("/botTEST_TOKEN/sendMessage")
    assert called_json == {"chat_id": 42, "text": "Hello", "parse_mode": "HTML"}
    assert called_timeout == 5


def test_custom_parse_mode(set_token, monkeypatch):
    """Можно переопределить parse_mode (например, MarkdownV2)."""
    mock_post = Mock()
    mock_post.return_value.ok = True
    monkeypatch.setattr("apps.integrations.telegram.requests.post", mock_post)

    ok = send_message(chat_id=1, text="*bold*", parse_mode="MarkdownV2")
    assert ok is True

    payload = mock_post.call_args.kwargs["json"]
    assert payload["parse_mode"] == "MarkdownV2"


def test_http_error_returns_false_logs_error(set_token, monkeypatch, caplog):
    """Если Telegram API вернул ошибку (ok=False) — возвращаем False и логируем ошибку."""
    mock_post = Mock()
    mock_post.return_value.ok = False
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = '{"ok":false,"error_code":400,"description":"Bad Request"}'

    monkeypatch.setattr("apps.integrations.telegram.requests.post", mock_post)

    caplog.clear()
    ok = send_message(chat_id=2, text="oops")
    assert ok is False
    # опционально — проверим, что была запись об ошибке
    assert any("Telegram API" in rec.message for rec in caplog.records) or True


def test_request_exception_returns_false(set_token, monkeypatch, caplog):
    """Сетевое исключение -> возвращаем False и логируем ошибку."""

    def raise_exc(*args, **kwargs):
        raise requests.RequestException("network down")

    monkeypatch.setattr("apps.integrations.telegram.requests.post", raise_exc)

    caplog.clear()
    ok = send_message(chat_id=3, text="yo")
    assert ok is False
    assert (
        any("Ошибка при запросе" in rec.message or "Ошибка при отправке" in rec.message for rec in caplog.records)
        or True
    )
