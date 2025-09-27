import logging
import os

import requests

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


def send_message(chat_id: int, text: str, parse_mode: str = "HTML") -> bool:
    """
    Отправка сообщения через Telegram Bot API.

    Args:
        chat_id (int): ID чата (обычно user.telegram_id).
        text (str): Текст сообщения.
        parse_mode (str): Режим форматирования ("HTML" или "MarkdownV2").

    Returns:
        bool: True, если сообщение успешно доставлено, False — при ошибке.
    """
    if not BOT_TOKEN:
        logger.warning("Попытка отправить сообщение без TELEGRAM_BOT_TOKEN")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        response = requests.post(
            url,
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=5,
        )
        if not response.ok:
            logger.error("Ошибка Telegram API %s: %s", response.status_code, response.text)
        return response.ok
    except requests.RequestException as e:
        logger.error("Ошибка при запросе в Telegram API: %s", e)
        return False
