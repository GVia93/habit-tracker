# Habit Tracker
Проект на **Django + DRF**  
Реализует регистрацию/авторизацию, CRUD привычек, публичный список привычек и интеграцию с **Telegram** для напоминаний (через Celery).

---

## Оглавление
- [Установка и запуск](#установка-и-запуск)
- [Redis + Celery](#redis--celery)
- [Запуск через Docker Compose](#запуск-через-docker-compose)
- [Основные эндпоинты](#основные-эндпоинты)
- [Интеграция с Telegram](#интеграция-с-telegram)
- [Документация API](#документация-api)
- [Тесты и стиль кода](#тесты-и-стиль-кода)
- [Переменные окружения](#переменные-окружения)
- [Настройка сервера (Ubuntu 22.04 + Docker + Nginx)](#настройка-сервера-ubuntu-2204--docker--nginx)
- [CI/CD (GitHub Actions)](#cicd-github-actions)
- [Архитектура проекта](#архитектура-проекта)
- [Обновление проекта](#обновление-проекта)


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


---

## Настройка сервера (Ubuntu 22.04 + Docker + Nginx)

1. **Установите зависимости**  
   На чистом сервере выполните:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y docker.io docker-compose nginx
   sudo systemctl enable docker
   ```

2. **Настройте доступ по SSH-ключам**  
   - Скопируйте ваш публичный ключ на сервер:
     ```bash
     ssh-copy-id user@your-server-ip
     ```
   - Запретите вход по паролю (в `/etc/ssh/sshd_config`):
     ```
     PasswordAuthentication no
     ```
   - Перезапустите SSH:
     ```bash
     sudo systemctl restart ssh
     ```

3. **Закройте ненужные порты**  
   Оставьте открытым только 22 (SSH) и 80/443 (HTTP/HTTPS):
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw allow 80
   sudo ufw allow 443
   sudo ufw enable
   ```

4. **Подготовьте директории проекта**  
   ```bash
   mkdir -p ~/apps/habit-tracker
   cd ~/apps/habit-tracker
   ```

5. **Настройте Docker Compose и окружение**  
   - Скопируйте файлы проекта на сервер (через `git pull` или `rsync`).  
   - Создайте файл `.env` на основе `.env.example`.  
   - Запустите проект:
     ```bash
     docker compose up -d --build
     ```

6. **Настройте Nginx**  
   - Добавьте конфиг (пример уже есть в `nginx.conf`).  
   - Скопируйте его в `/etc/nginx/sites-available/habit-tracker` и сделайте симлинк:
     ```bash
     sudo ln -s /etc/nginx/sites-available/habit-tracker /etc/nginx/sites-enabled/
     ```
   - Проверьте конфиг:
     ```bash
     sudo nginx -t
     ```
   - Перезапустите Nginx:
     ```bash
     sudo systemctl restart nginx
     ```

После этого приложение будет доступно по IP-адресу сервера или вашему домену.

---

## CI/CD (GitHub Actions)

Проект настроен на автоматический деплой при каждом push в репозиторий.

1. **Workflow-файл**  
   Находится в `.github/workflows/ci-cd.yml`.  
   Содержит шаги:
   - установка зависимостей,
   - запуск тестов (`pytest`, `flake8`),
   - деплой на сервер (только после успешного прохождения тестов).

2. **Secrets GitHub**  
   Для работы CI/CD необходимо задать секреты в репозитории:  
   - `HOST` — IP или домен сервера,  
   - `USERNAME` — пользователь для SSH,  
   - `SSH_KEY` — приватный ключ для доступа на сервер,  
   - другие переменные окружения (например, `DB_PASSWORD`, `TELEGRAM_BOT_TOKEN`).

3. **Запуск workflow**  
   Workflow запускается автоматически при `git push`.  
   Проверить статус можно в GitHub: вкладка **Actions** → выбранный workflow.

4. **Проверка деплоя**  
   После успешного выполнения workflow приложение будет доступно по адресу сервера.  
   Логи деплоя можно просмотреть в GitHub Actions.

   
---

## Архитектура проекта

```
        Nginx (reverse proxy, static/media)
                  |
          Gunicorn (Django)
                  |
       ------------------------
       |         |            |
    Postgres   Redis       Celery (beat + worker)
```

- **Nginx** — отдача статики/медиа, прокси до Django.  
- **Gunicorn** — WSGI сервер для Django.  
- **Postgres** — база данных.  
- **Redis** — брокер сообщений для Celery.  
- **Celery** — обработка фоновых задач и планировщик напоминаний.

---

## Переменные окружения

Основные переменные (см. `.env.example` для актуальных значений):

```ini
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,127.0.0.1

# База данных
DB_HOST=db
DB_PORT=5432
DB_NAME=habit_db
DB_USER=habit_user
DB_PASSWORD=superpassword

# Redis
REDIS_URL=redis://redis:6379/0

# Telegram
TELEGRAM_BOT_TOKEN=123456:AA...your-token

# Дополнительно
TIMEZONE=Europe/Moscow
```

---

## Обновление проекта

Для выката новых версий на сервере:

```bash
cd ~/apps/habit-tracker
git pull origin develop
docker compose up -d --build
docker compose exec web python manage.py migrate
```

---

## Настройка HTTPS (опционально)

Для продакшн рекомендуется включить HTTPS через **Let's Encrypt**:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

Сертификаты обновляются автоматически (cron уже установлен с certbot).
