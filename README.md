# Django API with Restrictions 📱

REST API для мобильного приложения с объявлениями. Полнофункциональный бэкенд с поддержкой аутентификации, ограничениями на запросы и системой управления объявлениями.

## 🚀 Основные возможности

- ✅ Создание и просмотр объявлений
- ✅ Фильтрация по статусу и дате создания
- ✅ Система избранных объявлений
- ✅ Три статуса объявлений: **OPEN**, **CLOSED**, **DRAFT**
- ✅ Токен-аутентификация
- ✅ Rate limiting (защита от ботов)
- ✅ Административные функции
- ✅ Валидация на максимум 10 открытых объявлений per пользователю

## 📋 Требования

- Python 3.8+
- Django 3.1+
- Django REST Framework
- PostgreSQL
- django-filter

## ⚙️ Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/amirlionheart/Django-APIwithRestrictions.git
cd Django-APIwithRestrictions
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Создание базы данных
Создайте PostgreSQL базу данных:
```bash
createdb netology_classified_ads
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: `http://localhost:8000/`

## 🔐 Аутентификация

Проект использует **Token Authentication**. 

### Получение токена:
1. Перейдите в админку: `http://localhost:8000/admin/`
2. Создайте пользователя (если его еще нет)
3. Перейдите в раздел **Tokens**
4. Создайте новый токен для пользователя

### Использование токена в запросах:
```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://localhost:8000/api/adv/
```

Или в Postman:
- **Header**: `Authorization`
- **Value**: `Token YOUR_TOKEN_HERE`

## 📊 API Endpoints

### Объявления

| Метод | Endpoint | Описание | Требует авторизацию |
|-------|----------|---------|---------------------|
| GET | `/api/adv/` | Список объявлений | ❌ Нет |
| POST | `/api/adv/` | Создать объявление | ✅ Да |
| GET | `/api/adv/{id}/` | Получить объявление | ❌ Нет* |
| PUT | `/api/adv/{id}/` | Обновить объявление | ✅ Да (только автор/админ) |
| PATCH | `/api/adv/{id}/` | Частичное обновление | ✅ Да (только автор/админ) |
| DELETE | `/api/adv/{id}/` | Удалить объявление | ✅ Да (только автор/админ) |

*Черновики (DRAFT) видны только автору

### Избранное

| Метод | Endpoint | Описание | Требует авторизацию |
|-------|----------|---------|---------------------|
| POST | `/api/adv/{id}/favorite/` | Добавить в избранное | ✅ Да |
| GET | `/api/adv/favorites/` | Получить избранные | ✅ Да |

## 🔍 Фильтрация объявлений

Используйте query параметры для фильтрации:

```bash
# По статусу
GET /api/adv/?status=OPEN

# По дате (после и до)
GET /api/adv/?created_at_after=2024-01-01&created_at_before=2024-12-31

# Комбинированная фильтрация
GET /api/adv/?status=OPEN&created_at_after=2024-01-01
```

### Доступные фильтры:
- `status` — OPEN, CLOSED, DRAFT
- `created_at_after` — объявления после даты (формат: YYYY-MM-DD)
- `created_at_before` — объявления до даты (формат: YYYY-MM-DD)

## ⏱️ Rate Limiting

Проект защищен от перегрузки с помощью rate limiting:

- **Неавторизованные пользователи**: 10 запросов в минуту
- **Авторизованные пользователи**: 20 запросов в минуту

При превышении лимита вернется ошибка `429 Too Many Requests`.

## 📝 Статусы объявлений

| Статус | Видимость | Описание |
|--------|-----------|---------|
| **OPEN** | Все пользователи | Открыто для просмотра и взаимодействия |
| **CLOSED** | Только автор | Закрыто, но остается в истории |
| **DRAFT** | Только автор | Черновик, не видно другим пользователям |

## ⚠️ Основные ограничения

- 📌 Один пользователь может иметь максимум **10 открытых объявлений**
- 🚫 Автор не может добавить своё объявление в избранное
- 🔒 Обновлять и удалять объявления может только автор или администратор
- ⏰ Rate limiting: 10 запросов/мин для анонимов, 20 запросов/мин для авторизованных

## 📂 Структура проекта

```
Django-APIwithRestrictions/
├── api_with_restrictions/       # Основной конфиг проекта
│   ├── settings.py              # Django настройки
│   ├── urls.py                  # URL маршруты
│   └── wsgi.py
├── advertisements/              # Приложение объявлений
│   ├── models.py                # БД модели (Advertisement, Favorite)
│   ├── views.py                 # ViewSet для API
│   ├── serializers.py           # Сериализаторы данных
│   ├── permissions.py           # Кастомные permissions
│   ├── filters.py               # Фильтры для объявлений
│   ├── admin.py                 # Django админка
│   └── apps.py
├── manage.py                    # Django менеджмент команды
└── requirements.txt             # Зависимости проекта
```

## 👨‍💻 Технологический стек

- **Framework**: Django 3.1+, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Token Authentication (rest_framework.authtoken)
- **Filtering**: django-filter
- **Throttling**: DRF built-in Rate Limiting

## 📖 Примеры использования

### Создание объявления
```bash
curl -X POST http://localhost:8000/api/adv/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 13",
    "description": "В отличном состоянии",
    "status": "OPEN"
  }'
```

### Получение списка объявлений
```bash
curl http://localhost:8000/api/adv/?status=OPEN
```

### Добавление в избранное
```bash
curl -X POST http://localhost:8000/api/adv/1/favorite/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Получение избранных объявлений
```bash
curl http://localhost:8000/api/adv/favorites/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## ✨ Реализованные дополнительные задания

- ✅ **Права для админов** — Администраторы могут менять и удалять любые объявления
- ✅ **Избранные объявления** — Полная система добавления/удаления избранного
- ✅ **Статус DRAFT** — Черновики видны только автору

## 📄 Лицензия

MIT

## 👤 Автор

[amirlionheart](https://github.com/amirlionheart)

---

**Последнее обновление**: 2024
