FROM python:3.12-bullseye

WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

# Копируем проект
COPY project /app

WORKDIR /app

EXPOSE 8000

# Запускаем приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
