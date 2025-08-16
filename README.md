# 🛒 EShop - Бэкенд интернет-магазина

## 📖 Описание проекта

EShop - это бэкенд интернет-магазина, построенный на FastAPI и современном стеке технологий. Проект представляет собой REST API для управления товарами, пользователями, корзиной, заказами и комментариями.

## 🚀 Основные возможности

- **Аутентификация и авторизация** - JWT токены, OAuth2, подтверждение email
- **Управление товарами** - CRUD операции для товаров и категорий
- **Корзина покупок** - добавление, удаление, пакетные операции
- **Система заказов** - создание и управление заказами
- **Комментарии и отзывы** - система комментариев к товарам
- **Управление пользователями** - регистрация, профили, роли (admin/user)
- **Кэширование** - Redis для повышения производительности
- **Rate limiting** - защита от DDoS атак
- **Email уведомления** - Celery + ProtonMail для подтверждения регистрации
- **Миграции БД** - Alembic для управления схемой базы данных

## 🛠 Технологический стек

### Backend
- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **Alembic** - миграции базы данных
- **Pydantic** - валидация данных и сериализация
- **Uvicorn** - ASGI сервер
- **Python 3.13** - версия Python

### База данных
- **PostgreSQL** - основная реляционная база данных
- **Redis** - кэширование

### Аутентификация и безопасность
- **JWT** - JSON Web Tokens для аутентификации
- **bcrypt** - хеширование паролей
- **FastAPI Limiter** - ограничение частоты запросов

### Дополнительные сервисы
- **Celery** - фоновые задачи и очереди сообщений
- **ProtonMail API** - отправка email уведомлений для подтверждения регистрации

### Тестирование
- **pytest** - фреймворк для тестирования
- **httpx** - HTTP клиент для тестов

## 🔒 Безопасность и производительность

### Безопасность
- **JWT токены** - безопасная аутентификация
- **bcrypt** - хеширование паролей
- **Rate limiting** - защита от DDoS атак
- **CORS** - контроль доступа к API
- **Роли пользователей** - admin/user разделение прав

### Производительность
- **Redis кэширование** - ускорение HTTP ответов
- **Асинхронные операции** - FastAPI + async/await
- **Пакетные операции** - batch CRUD для корзины
- **Connection pooling** - эффективное управление соединениями БД

## 📊 Структура базы данных

### Основные таблицы
- **users** - пользователи системы (admin/user роли, подтверждение email)
- **products** - товары магазина с категориями
- **categories** - категории товаров
- **cart_items** - корзина покупок пользователей
- **orders** - заказы пользователей
- **comments** - комментарии к товарам
- **jwt_token_pairs** - JWT токены для аутентификации

### Связи между таблицами
- Пользователи могут иметь множество товаров в корзине
- Заказы связаны с пользователями и товарами
- Комментарии привязаны к товарам и пользователям
- Товары принадлежат категориям

## 🏗 Архитектура проекта

```
EShop/
├── app/
│   ├── api/           # API роутеры (FastAPI endpoints)
│   ├── auth/          # Аутентификация и OAuth
│   ├── core/          # Конфигурация и настройки
│   ├── database/      # Подключение к БД и Redis
│   ├── models/        # SQLAlchemy модели (ORM)
│   ├── schemas/       # Pydantic схемы для валидации
│   ├── services/      # Бизнес-логика приложения
│   ├── tasks/         # Celery задачи (email, etc.)
│   ├── tests/         # Тесты для API и сервисов
│   └── utils/         # Вспомогательные утилиты
├── migrations/         # Alembic миграции БД
├── docker-compose.yml  # Docker конфигурация
├── Dockerfile         # Docker образ
└── main.py            # Точка входа приложения
```

## 🔧 Как работает система

### 1. Структура API
- **`/api/auth`** - аутентификация и регистрация
- **`/api/products`** - управление товарами
- **`/api/categories`** - управление категориями
- **`/api/users`** - управление пользователями
- **`/api/cart_items`** - корзина покупок
- **`/api/orders`** - система заказов
- **`/api/comments`** - комментарии к товарам

### 2. Аутентификация
- JWT токены (access + refresh)
- Роли пользователей (admin/user)
- OAuth2 интеграция
- Защищенные эндпоинты для администраторов

### 3. Кэширование
- Redis для HTTP ответов
- Настраиваемое время жизни кэша
- Автоматическое обновление при изменениях

### 4. Безопасность
- Rate limiting для защиты от атак
- Валидация входных данных (Pydantic)
- Хеширование паролей (bcrypt)
- CORS настройки

## 🚀 Как запустить проект

### Предварительные требования
- Docker и Docker Compose
- Python 3.13+
- .env файл с настройками

### 1. Клонирование и настройка
```bash
git clone https://github.com/marsky0/EShop
cd EShop
```

### 2. Настройка .env файла
```bash
# Файл .env уже есть в репозитории
# Заполните в нем необходимые переменные окружения
```

### 3. Запуск через Docker (рекомендуется)
```bash
# Запуск всех сервисов в фоне
docker-compose up -d

# Или запуск с выводом логов в терминале
docker-compose up

# Просмотр логов (если запущено в фоне)
docker-compose logs -f

# Остановка
docker-compose down
```

### 4. Запуск локально
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск PostgreSQL и Redis (через Docker)
docker-compose up -d db redis
# Или используйте локальные

# Применение миграций
alembic upgrade head

# Запуск приложения
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Запуск Celery worker (в отдельном терминале)
celery -A app.tasks worker --loglevel=info
```

## 🐳 Docker и развертывание

### Dockerfile особенности
- **Python 3.13-slim** - легковесный образ Python
- **Автоматические миграции** - Alembic запускается при старте контейнера
- **Celery + Uvicorn** - оба сервиса запускаются в одном контейнере
- **entrypoint.sh** - скрипт инициализации с миграциями и запуском сервисов

### Docker Compose сервисы
- **web** - основное приложение (FastAPI + Celery)
- **db** - PostgreSQL 15 с персистентным хранилищем
- **redis** - Redis 7 для кэширования и очередей

### Переменные окружения для Docker
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/ESHOP
REDIS_URL=redis://redis:6379/
```

### 5. Проверка работоспособности
```bash
# API доступен по адресу
http://localhost:8000

# Документация Swagger
http://localhost:8000/docs

# Альтернативная документация ReDoc
http://localhost:8000/redoc
```

## 🔒 Переменные окружения

Создайте файл `.env` со следующими переменными:

```env
# Frontend
FRONTEND_URL=http://localhost:3000

# Rate Limiting
DEFAULT_RATELIMIT_NUM=100
DEFAULT_RATELIMIT_TIME=60

# JWT
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES=30
REFRESH_TOKEN_EXPIRES=1440

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ESHOP
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_URL=redis://localhost:6379
CACHE_EXPIRE_HTTP_RESPONSE=300

# Email
EMAIL_USER=your-email@protonmail.com
EMAIL_PASSWORD=your-email-password
```

## 📝 API Endpoints

### 🔐 Аутентификация
- `POST /api/auth/register` - Регистрация пользователя
- `GET /api/auth/confirm/{token}` - Подтверждение регистрации
- `POST /api/auth/login` - Вход в систему
- `POST /api/auth/logout` - Выход из системы
- `POST /api/auth/refresh` - Обновление токена

### 🛍️ Товары
- `GET /api/products/` - Список товаров
- `GET /api/products/{id}` - Получение товара по ID
- `POST /api/products/` - Создание товара (admin)
- `PUT /api/products/{id}` - Обновление товара (admin)
- `DELETE /api/products/{id}` - Удаление товара (admin)

### 📂 Категории
- `GET /api/categories/` - Список категорий
- `GET /api/categories/{id}` - Получение категории по ID
- `POST /api/categories/` - Создание категории (admin)
- `PUT /api/categories/{id}` - Обновление категории (admin)
- `DELETE /api/categories/{id}` - Удаление категории (admin)

### 🛒 Корзина покупок
- `GET /api/cart_items/` - Просмотр корзины (admin)
- `GET /api/cart_items/{id}` - Получение элемента корзины по ID (admin)
- `GET /api/cart_items/user_id/{user_id}` - Корзина пользователя
- `POST /api/cart_items/` - Добавление товара в корзину
- `POST /api/cart_items/batch/` - Пакетное добавление товаров
- `PUT /api/cart_items/{id}` - Обновление элемента корзины
- `PUT /api/cart_items/batch/` - Пакетное обновление элементов
- `DELETE /api/cart_items/{id}` - Удаление товара из корзины
- `DELETE /api/cart_items/batch/` - Пакетное удаление товаров

### 📋 Заказы
- `GET /api/orders/` - Список заказов
- `GET /api/orders/{id}` - Детали заказа
- `POST /api/orders/` - Создание заказа
- `PUT /api/orders/{id}` - Обновление заказа
- `DELETE /api/orders/{id}` - Удаление заказа

### 👥 Пользователи
- `GET /api/users/` - Список пользователей (admin)
- `GET /api/users/{id}` - Профиль пользователя
- `POST /api/users/` - Создание пользователя (admin)
- `PUT /api/users/{id}` - Обновление пользователя (admin)
- `DELETE /api/users/{id}` - Удаление пользователя (admin)

### 💬 Комментарии
- `GET /api/comments/` - Список комментариев
- `GET /api/comments/{id}` - Получение комментария по ID
- `POST /api/comments/` - Создание комментария
- `PUT /api/comments/{id}` - Обновление комментария
- `DELETE /api/comments/{id}` - Удаление комментария

## 🚀 Разработка и развертывание

### Локальная разработка
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск только БД и Redis
docker-compose up -d db redis

# Применение миграций
alembic upgrade head

# Запуск приложения с автоперезагрузкой
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Запуск Celery worker
celery -A app.tasks worker --loglevel=info
```

### Продакшен развертывание
```bash
# Сборка и запуск всех сервисов
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f web

# Остановка
docker-compose down
```

