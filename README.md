# Продуктовый помощник

## Описание
На проекте можно 
- создавать свои рецепты
- подписываться на рецепты других авторов
- добавлять рецепты в избранное
- класть ингридиенты рецептов в корзину
- скачивать список продуктов в .txt формате

Стек: Django Rest Framework, djoser аутентификация по токену, redoc, pagination, permissions, throttling, django_filters, docker-compose, nginx, postgreql

## Как запустить проект:
1. Kлонируем репозиторий:
```
git clone {project_link}
```

2. Поднимаем docker контейнеры
```
cd infra
docker compose up -d
```

3. Находим id контайнера и заходим в него
```
docker container ls
docker exec -it {container_id} bash
```

4. Выполняем команды
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py import_demo_data
python manage.py createsuperuser
```

Проект запущен!

## Документация к API:
Здесь описаны все доступные ендпоинты и примеры запросов к ним:
http://127.0.0.1/api/docs/redoc.html
