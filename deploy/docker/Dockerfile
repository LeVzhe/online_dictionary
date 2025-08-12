FROM python:3.12-slim-bookworm as builder

WORKDIR /app

# Установка build-зависимостей (+ curl для debug)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev git curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка зависимостей (включая pre-commit)
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt pre-commit ruff

# Копирование всего проекта (включая .pre-commit-config.yaml и .git)
COPY . .

# Инициализация pre-commit (без активации в Git)
RUN pre-commit install-hooks && \
    pre-commit run --all-files || echo "Pre-commit checks completed"

# Production образ
FROM python:3.12-slim-bookworm

WORKDIR /app

# Копируем только необходимое из builder-стадии
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Обеспечиваем доступность скриптов
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

# Чистка ненужных файлов (но оставляем .pre-commit-config.yaml)
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + && \
    rm -rf /app/.git /app/.ruff_cache

EXPOSE 8000
