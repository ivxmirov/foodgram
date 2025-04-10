# [Foodgram - Ваша кулинарная книга](https://github.com/ivxmirov/foodgram.git) 🍳

**Foodgram** — это платформа для обмена рецептами ваших любимых блюд с другими пользователями. Пользователи Foodgram могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Зарегистрированным пользователям также доступен сервис «Список покупок»: он создает список продуктов, которые нужно купить для приготовления выбранных блюд.
<br><hr>

### Возможности:
- **Главная страница:** список рецептов с постраничной пагинацией и сортировкой по дате публикации.
- **Страница рецепта:** подробная информация о рецепте с возможностью добавить в избранное или покупки.
- **Страница пользователя:** список рецептов конкретного автора с возможностью подписки.
- **Избранное:** управление списком любимых рецептов.
- **Список покупок:** формирование и скачивание списка необходимых ингредиентов для выбранных рецептов.
- **Создание рецептов:** доступно авторизованным пользователям с полным контролем над своими публикациями.
- **Фильтрация по тегам:** удобный поиск рецептов по категориям.
- **Регистрация и авторизация:** включая возможность восстановления пароля.

---

### Уровни доступа:
- **Гости:** могут просматривать рецепты и страницы пользователей.
- **Авторизованные пользователи:** имеют доступ ко всем возможностям, включая создание рецептов, добавление в избранное и покупки, подписки.
- **Администраторы:** полный контроль над системой, включая редактирование и удаление любого контента.

---

### Технологии:
- **Backend:**
  - ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  - ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
  - ![Django REST Framework](https://img.shields.io/badge/Django%20REST-092E20?style=for-the-badge&logo=django&logoColor=white)
  - ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
  - ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
- **Frontend:**
  - ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
- **Инфраструктура:**
  - ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
  - ![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
  - ![Docker Compose](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
  - ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
  
---

### Разворачивание проекта:
Деплой проекта осуществляется автоматически при внесении изменений и пуше 
в ветку **main** репозитория на GitHub.

#### Разворачивание сервиса автоматически
1. Настройка окружения:
Создайте файл `.env` в корне проекта со следующими переменными:
```env
SECRET_KEY=<секретный_ключ>
DEBUG=False
ALLOWED_HOSTS=<разрешенные_хосты>
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=<имя_базы>
POSTGRES_USER=<пользователь_базы>
POSTGRES_PASSWORD=<пароль>
DB_HOST=db
DB_PORT=5432
```

2. **При пуше в ветку `main`:**
    - Запускаются тесты и линтеры для проверки качества кода.
    - Собираются Docker-образы приложения.
    - Образы пушатся на Docker Hub.
  
3. **После успешной сборки:**
    - Подключается сервер.
    - Копируется и запускается файл `docker-compose.production.yml`.
    - Выполняются миграции и сборка статики.
  
4. **Уведомление:**
    - После успешного деплоя отправляется уведомление в Telegram-бот о завершении процесса.

#### Разворачивание сервиса на сервере вручную

1. Подготовьте файл `.env` в корне проекта с переменными.
2. Запустите проект, используя файл `docker-compose.production.yml`:
 ```bash
    docker compose -f docker-compose.production.yml up -d
 ```
3. Выполните миграции базы данных:
 ```bash
    docker compose -f docker-compose.production.yml exec backend python manage.py migrate
 ```
4. При необходимости наполните БД Списком ингредиентов (backend/data/):
 ```bash
    docker compose -f docker-compose.production.yml exec backend python manage.py imort_data
 ```
5. Соберите и скопируйте статику:
 ```bash
    docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
 ```
---

### Некоторые примеры запросов к API 

#### Профиль пользователя

Доступно всем пользователям

__GET__ http://localhost/api/users/{id}/

Response:
```
{
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
}
```

#### Создание рецепта

Доступно только авторизованному пользователю

__POST__ http://localhost/api/recipes/

Request:
```
{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```

Response:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Иванов",
    "is_subscribed": false,
    "avatar": "http://foodgram.example.org/media/users/image.png"
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "text": "string",
  "cooking_time": 1
}
```

#### Добавить рецепт в список покупок
Доступно только авторизованным пользователям

__POST__ http://localhost/api/recipes/{id}/shopping_cart/

Response:
```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "cooking_time": 1
}
```

#### Добавить рецепт в избранное
Доступно только авторизованному пользователю

__POST__ http://localhost/api/recipes/{id}/favorite/

Response:
```
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.png",
  "cooking_time": 1
}
```

#### Подписаться на пользователя
Доступно только авторизованным пользователям

__POST__ http://localhost/api/users/{id}/subscribe/

Response:
```
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Иванов",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.png",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0,
  "avatar": "http://foodgram.example.org/media/users/image.png"
}
```

### Автор
Хмыров Илья - [GitHub](https://github.com/ivxmirov)
