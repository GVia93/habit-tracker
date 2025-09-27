# Базовый образ: Python 3.13 (слой slim — минимальный Debian)
FROM python:3.13-slim

# Переменные окружения для Python/Pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Рабочая директория
WORKDIR /app

# Системные зависимости для psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости (отдельно, чтобы использовать кэш)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Копируем проект
COPY . .

# Создаём пользователя и назначаем права (не root)
RUN useradd -m appuser \
    && chown -R appuser:appuser /app
USER appuser

# Пробрасываем порт Gunicorn
EXPOSE 8000
