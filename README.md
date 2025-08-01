**Описание**

Это простое full-stack веб-приложение, состоящее из двух частей:

- **Backend** на FastAPI, обрабатывающий запросы к API OpenRouter/OpenAI.
- **Frontend** на Nuxt 3 с Tailwind CSS, обеспечивающий минималистичный интерфейс с поддержкой голосового ввода через Web Speech API.

Приложение позволяет пользователю:

1. Вводить текстовый запрос.
2. Отправлять запрос к AI-сервису.
3. Получать и отображать ответ.
4. Использовать голосовой ввод для формирования запроса.

---

## Структура проекта

```
test-task-gptchat-app/
├── backend/         # FastAPI сервер
│   ├── app/
│   │   ├── api.py
│   │   └── services/
│   │       └── chatgpt.py
│   ├── .env
│   ├── main.py
│   └── requirements.txt
└── frontend/        # Nuxt 3 приложение
    ├── components/
    │   └── ChatInput.vue
    │      
    ├── composables/
    │   ├── useChat.ts
    │   └── useSpeechRecognition.ts
    ├── app/
    │   └── app.vue
    ├── public/
    ├── .env
    ├── nuxt.config.ts
    ├── package.json
    └── tailwind.config.js
```

---

## Backend (FastAPI)

### Пререквизиты

- Python 3.12+
- pip 25.2

### Установка зависимостей

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Переменные окружения

Создайте файл `.env` в папке `backend/` с содержимым:

```dotenv
AI_API_KEY=ваш_ключ_OpenRouter_или_OpenAI
BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=deepseek/deepseek-chat-v3-0324:free
```

### Запуск сервера

```bash
uvicorn main:app --reload --port 8000
```

**Эндпоинты**

- `POST /api/chat` — принимает JSON `{ "text": "..." }`, возвращает `{ "reply": "..." }`.

**Обработка ошибок**

- 401 — ошибка авторизации.
- 429 — превышен лимит запросов.
- 408 — таймаут.
- 502/503 — временная недоступность.

---

## Frontend (Nuxt 3/4)

### Установка зависимостей

```bash
cd frontend
npm install
```

### Переменные окружения

Создайте файл `.env` в папке `frontend/` с содержимым:

```dotenv
API_BASE=http://localhost:8000
```


### Конфигурация

В `nuxt.config.ts` проверьте, что `apiBase` установлен:

```ts
export default defineNuxtConfig({
  runtimeConfig: {
    public: { apiBase: process.env.API_BASE }
  }
})
```

### Запуск приложения

```bash
npm run dev
```
