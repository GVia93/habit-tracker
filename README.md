# Habit Tracker
Проект на **Django + DRF**  
Реализует регистрацию/авторизацию, CRUD привычек, публичный список привычек и интеграцию с **Telegram** для напоминаний (через Celery).

---

## Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone <URL>
cd habit-tracker

# 2. Создать виртуальное окружение
python -m venv .venv
.venv\Scripts\activate   # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env
cp .env.example .env

# 5. Применить миграции
python manage.py migrate

# 6. Создать суперпользователя (опционально)
python manage.py create_superuser

# 7. Запустить сервер
python manage.py runserver
```

---

## Redis + Celery

Для работы напоминаний нужен Redis.


Запуск Celery:

```bash
celery -A config worker -l info -P solo   # worker
celery -A config beat -l info             # планировщик
```
## Запуск через Docker Compose

```bash
# 1) Подготовка
cp .env.example .env
# при необходимости отредактируйте .env

# 2) Запуск всех сервисов
docker compose up --build -d

# 3) Создать суперпользователя
docker compose exec web python manage.py create_superuser
```
---

## Основные эндпоинты

### Аутентификация
- `POST /auth/register/`
- `POST /auth/login/`
- `POST /auth/refresh/`

### Привычки
- `GET /habits/` — список привычек текущего пользователя (пагинация по 5).
- `POST /habits/` — создание привычки.
- `GET /habits/public/` — публичные привычки (без авторизации).
- `GET/PUT/DELETE /habits/{id}/`

### Telegram
- `GET /integrations/telegram-profiles/` — свой профиль.
- `POST /integrations/telegram-profiles/` — создать/обновить привязку.

---

## Интеграция с Telegram

1. Получи токен бота у [@BotFather](https://t.me/botfather).  
2. Добавь его в `.env`:  
   ```
   TELEGRAM_BOT_TOKEN=123456:AA...your-token
   ```
3. Напиши своему боту хоть одно сообщение.  
4. Узнай свой `chat_id`.  
5. Создай `TelegramProfile` через API или Django Admin.  
6. Сообщения начнут приходить автоматически в момент привычки.

---

## Документация API

- Swagger: [`/swagger/`](http://127.0.0.1:8000/swagger/)
- ReDoc: [`/redoc/`](http://127.0.0.1:8000/redoc/)

---

## Тесты и стиль кода

```bash
pytest --cov=apps --cov-report=term-missing
flake8 --exclude=migrations
black . --check
```

---

## Переменные окружения

См. [.env.example](.env.example). Основные:

```
