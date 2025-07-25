# Используем официальный образ Python
FROM python:3.13.3-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем poetry
RUN pip install poetry

# Устанавливаем зависимости проекта (без dev-зависимостей)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем оставшийся код приложения
COPY . .

# Открываем порт
EXPOSE 8000

# Команда запуска приложения
CMD ["uvicorn", "ai_analyzer.main:app", "--host", "0.0.0.0", "--port", "8000"]
