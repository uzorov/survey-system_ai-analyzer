# AI Analyzer

## Описание
Сервис для анализа текстовых запросов клиентов на закупку промышленных труб с помощью искусственного интеллекта. Сервис извлекает ключевые параметры из текста и классифицирует уровень интереса клиента.

## Требования
- Docker и Docker Compose
- Доступ к интернету для загрузки Docker-образов и работы с Hugging Face API
- Токен доступа Hugging Face (https://huggingface.co/settings/tokens)

## Быстрый старт (рекомендуется)

### 1. Клонируйте репозиторий
```bash
git clone <URL-репозитория>
cd ai_analyzer
```

### 2. Установите переменные окружения

Создайте файл `.env` в корне проекта и добавьте в него ваш токен Hugging Face:

```
HF_API_TOKEN=hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> **Важно!** Не используйте токен из примера. Получите свой токен на https://huggingface.co/settings/tokens

### 3. Запустите сервис через Docker Compose

```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:17304

## Ручной запуск (без Docker)

1. Установите Python 3.13+
2. Установите Poetry:
   ```bash
   pip install poetry
   ```
3. Установите зависимости:
   ```bash
   poetry install --no-root
   ```
4. Создайте файл `.env` с переменной `HF_API_TOKEN` (см. выше).
5. Запустите сервер:
   ```bash
   uvicorn ai_analyzer.main:app --host 0.0.0.0 --port 8000
   ```

## Описание API

### POST `/analyze`
- **Описание:** Анализирует текст и возвращает извлечённые параметры.
- **Тело запроса:**
  ```json
  {
    "text": "<текст запроса клиента>"
  }
  ```
- **Ответ:**
  ```json
  {
    "type_of_pipe": "Бесшовная",
    "diameter_of_pipe": "До 500 мм",
    "pipe_wall_thickness": "До 15 мм",
    "volume_tons": "До 100 т.",
    "timeline": "До месяца",
    "interest_level": "HOT"
  }
  ```

### POST `/analyze_param?param_code=<код_параметра>`
- **Описание:** Анализирует текст и возвращает только указанный параметр.
- **Возможные значения `param_code`:**
  - `type_of_pipe`
  - `diameter_of_pipe`
  - `pipe_wall_thickness`
  - `volume_tons`
  - `timeline`
  - `interest_level`
- **Тело запроса:**
  ```json
  {
    "text": "<текст запроса клиента>"
  }
  ```
- **Ответ:**
  ```json
  {
    "type_of_pipe": "Бесшовная"
  }
  ```

## Переменные окружения
- `HF_API_TOKEN` — токен доступа Hugging Face (обязателен)

## Примечания
- Для работы сервиса требуется стабильное интернет-соединение.
- Все зависимости устанавливаются автоматически при сборке Docker-образа.
- Для продакшн-развёртывания рекомендуется использовать Docker.

---

## Автор
**Узоров Кирилл Александрович**  
Ведущий разработчик
Email: kirill.uzorov@tmk-group.com
