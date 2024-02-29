# Backend BestExchangeBot
Включает в себя: Админ панель и API сервис

---
Подразумевается, что на компьютере установлены Docker, docker-compose, Git.
Версии, используемые при разработке:
- Docker - 24.0.7
- Docker-compose - 1.29.2
- Git - 2.34.1
---

# Используемые инструменты(фреймворки и библиотеки)
---
- Django: для реализации админ панели
- Django ORM: для взаимодействия с БД
- FastAPI: для реализации REST API сервиса
- PostgreSQL: реляционная БД
- Redis: хранилище данных для очереди фоновых задач и кэша
- Celery: для реализации фоновых задач
- Django-celery-beat: для реализации периодических фоновых задач
- Selenium: для имитации работы пользователя в браузере, парсинг отзывов/комментариев обменников
- Uvicorn: ASGI веб-сервер
---

# Инструкция по сборке проекта

Склонируйте репозиторий к себе:
```
git clone https://github.com/TelegramMiniApps-2023/bestexchange_back.git
```
Перейдите в папку проекта:
```
cd bestexchange_back/ && cd django_fastapi/
```
---
Откройте файл .env:
```
nano .env
```

Добавьте в файл .env следующее содержимое:
```
#DATABASE
DB_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
DB_PORT=
DB_NAME=

#DJANGO ADMIN
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_PASSWORD=
DJANGO_SUPERUSER_EMAIL=

#DJANGO SETTINGS
CSRF_TOKEN=

#SELENIUM
SELENIUM_DRIVER=

#REDIS
REDIS_HOST=
REDIS_PASSWORD=
REDIS_PORT=
```

Выйдите и сохраните файл .env:
- нажмите Ctrl + X
- подтвердите изменения нажав Y
- нажмите Enter
---

# Конфигурация docker-compose файла

***При первом запуске***
---

command для сервиса django_fastapi:
```
services:

  django_fastapi:
    ...
    ...
    command: sh -c "python manage.py makemigrations &&
                    python manage.py migrate &&
                    python manage.py collectstatic --no-input &&
                    python manage.py loaddata media/base_db.json &&
                    python manage.py loaddata media/countries.json &&
                    python manage.py create_periodic_task_for_delete_reviews &&
                    python manage.py create_cities &&
                    python manage.py create_moderator_group &&
                    python manage.py periodic_task_for_parse_cash_courses &&
                    python manage.py createsuperuser --no-input &&
                    python manage.py parse_reviews_selenium &&
                    uvicorn project.asgi:app --host 0.0.0.0"
```
---

***При повторных запусках***
---
Предполагается, что БД уже была подключена и наполнена при первом запуске!

Предполагается, что volume postgres-data, redis_data, static и media существуют после первого запуска!

command для сервиса django_fastapi:
```
services:

  django_fastapi:
    ...
    ...
    command: sh -c "python manage.py makemigrations &&
                    python manage.py migrate &&
                    uvicorn project.asgi:app --host 0.0.0.0"
                    #python manage.py collectstatic --no-input &&
                    #python manage.py loaddata media/base_db.json &&
                    #python manage.py loaddata media/new_country.json &&
                    #python manage.py create_periodic_task_for_delete_reviews &&
                    #python manage.py create_cities &&
                    #python manage.py create_moderator_group &&
                    #python manage.py periodic_task_for_parse_cash_courses &&
                    #python manage.py createsuperuser --no-input &&
                    #python manage.py parse_reviews_selenium &&
```
---

**Перед сборкой убедитесь, что service Docker активен!**

Соберите docker-compose:
```
docker-compose build
```
Запустите сборку:
```
docker-compose up -d
```
Адрес админ панели: {домен / ip-адрес}/django/admin/

Адрес API Swagger: {домен / ip-адрес}/docs

Адрес API: {домен / ip-адрес}/api/{endpoint}