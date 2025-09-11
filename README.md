habit-tracker/
├─ config/                  # settings, celery, urls, asgi/wsgi
├─ apps/
│  ├─ users/                # кастомный User, auth
│  ├─ habits/               # Habit, CRUD, публичный список
│  └─ integrations/         # TelegramProfile, задачи Celery, Telegram API
├─ utils/                   # пагинация, permissions и прочие утилиты
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ pytest.ini
└─ README.md
