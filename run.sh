#!/bin/bash

# Проверяем, что была передана хотя бы одна команда
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 like {up|upf|down|manage [args] .. others}"
    exit 1
fi

case "$1" in
# Для докера
    build)
        echo "Rebuilding Docker Compose..."
        cd deploy || exit
        docker compose build
        ;;
    up)
        echo "Starting Docker Compose..."
        cd deploy || exit
        docker compose up -d
        ;;
    upf)
        echo "Starting Docker Compose with force recreate..."
        cd deploy || exit
        docker compose up -d --force-recreate
        ;;
    down)
        echo "Closing Docker Compose..."
        cd deploy || exit
        docker compose down
        ;;
# Для линтера
    lint)
        echo "Run Linter..."
        cd deploy || exit
        docker compose exec web-app ruff check --fix --extend-select I .
        ;;

# Для сервисов джанго
    manage)
        cd deploy || exit
        shift # Сдвигаем аргументы влево, чтобы $2 стал $1, $3 стал $2 и т.д.
        echo "Executing manage.py command in the container..."
        docker compose exec web-app python manage.py "$@"
        ;;
    shell)
        cd deploy || exit
        docker compose exec web-app python manage.py shell -i ipython
        ;;
# Установка зависимости
    pip)
        shift # Сдвигаем аргументы влево, чтобы $2 стал $1, $3 стал $2 и т.д.
        echo "Installing requirements..."
        pip install "$@"
        pip freeze > requirements.txt
        echo "Installing requirements COMPLETE"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
