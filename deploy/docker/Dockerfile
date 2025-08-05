FROM python:3.12-slim-bookworm as builder

WORKDIR /app

# Установка build-зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Установка и запуск pre-commit с Ruff
RUN pip install --user pre-commit ruff && \
    python -m ruff check . --fix && \
    python -m ruff format .

# Production образ
FROM python:3.12-slim-bookworm

WORKDIR /app

# Копируем только необходимое из builder-стадии
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Обеспечиваем доступность скриптов из .local
ENV PATH=/root/.local/bin:$PATH

# Чистка ненужных файлов
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + && \
    rm -rf /app/.git /app/.ruff_cache

EXPOSE 8000

# Запуск приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]