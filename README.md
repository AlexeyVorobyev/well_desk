# Well Desk

Описание продукта
-----------------
Well Desk — персональный ассистент для заботы о самочувствии на рабочем месте. Он помогает фиксировать
состояние, вести короткий диалог с советами, планировать приём лекарств и сохранять профиль, чтобы
рекомендации оставались персонализированными. Проект разработан Мочаловой Екатериной Алексеевной.

Ключевой функционал
-------------------
- **Профиль пользователя**: сбор данных о режиме работы, предпочтениях по перерывам и базовой информации
  для персонализации подсказок. 【F:frontend/src/components/ProfileForm.tsx†L15-L118】
- **Оценка самочувствия**: форма фиксации усталости, энергии, концентрации и заметок для отслеживания
  динамики. 【F:frontend/src/components/WellbeingForm.tsx†L1-L161】
- **Диалог с ассистентом**: хранение истории сообщений и генерация ответов по контексту пользовательских
  запросов. 【F:frontend/src/components/MessagesPanel.tsx†L1-L115】【F:backend/app/routers/messages.py†L1-L35】
- **Напоминания о лекарствах**: создание расписания, учёт приёма и история логов. 【F:frontend/src/components/MedicationRemindersDock.tsx†L1-L176】【F:backend/app/routers/medications.py†L1-L52】
- **База знаний**: подборка быстрых советов по здоровому рабочему дню. 【F:frontend/src/components/KnowledgeBase.tsx†L1-L40】

Структура проекта
-----------------
```
well_desk/
├── backend/            # FastAPI-приложение, модели, сервисы и репозитории
├── frontend/           # Клиент на React + Vite с компонентами интерфейса
└── README.md           # Этот документ
```

Архитектура и технологии
------------------------
- **Frontend**: React 18 + TypeScript, Vite, Material UI, React Router, TanStack Query для работы с API. 【F:frontend/src/main.tsx†L1-L22】【F:frontend/src/components/AppLayout.tsx†L1-L19】
- **Backend**: FastAPI, Pydantic, SQLAlchemy (async) с инициализацией схем при старте приложения. 【F:backend/app/main.py†L1-L36】
- **Слои бэкенда**: DTO (Pydantic-модели), routers, services, repositories и компоненты (БД, LLM). 【F:backend/app/main.py†L1-L36】【F:backend/app/components/database.py†L1-L62】
- **Данные**: SQLite (через SQLAlchemy) и миграции Alembic, конфигурация через Pydantic Settings. 【F:backend/alembic/env.py†L1-L39】【F:backend/app/settings.py†L1-L73】

Запуск проекта локально
 -----------------------
 1. **Backend**
    ```bash
    cd backend
    bash run.sh
    ```
 2. **Frontend**
    ```bash
    cd frontend
   npm install
   npm run dev
   ```

Полезные эндпоинты
------------------
- `GET /api/profile` и `PUT /api/profile` — чтение и сохранение профиля. 【F:backend/app/routers/profile.py†L10-L22】
- `GET /api/wellbeing` и `PUT /api/wellbeing` — получение и фиксация показателей самочувствия. 【F:backend/app/routers/wellbeing.py†L10-L25】
- `GET /api/messages` и `POST /api/messages` — история и отправка пользовательских сообщений; `POST /api/messages/llm` — ответ ассистента. 【F:backend/app/routers/messages.py†L1-L35】
- `POST /api/medications`, `GET /api/medications`, `DELETE /api/medications/{id}` — управление напоминаниями; `POST /api/medications/{id}/log` и `GET /api/medications/logs` — учёт приёма. 【F:backend/app/routers/medications.py†L1-L52】

