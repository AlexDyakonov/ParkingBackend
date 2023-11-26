Данный репозиторий является частью проекта, направленного на решение задачи хакатона "Урбатон" по треку "Оптимизация
парковочных мест"

---
Инструкция по запуску

- [development](#запуск-development)
- [production](#запуск-production)
---
[API DOCS](API_docs.md)

---
## Запуск development

Необходимо создать в корне .env файл, который состоит из:

    DJANGO_SECRET_KEY=secret-key
    ALLOWED_HOST=127.0.0.1
    
    # Без юкассы не будет работать бронирование
    YOOKASSA_ACCOUNT_ID=<integer>
    YOOKASSA_SECRET_KEY=<string>

Запуск дев сервера 
    
    python manage.py runserver

## Запуск production

В продакшне запускается с помощью docker compose

Для запуска в докере необходимо в корне директории создать .env.docker

    DJANGO_SECRET_KEY=django-insecure-lxz7knx5^&jku*(hp@^uw2lx!eqp0a1_lzp0@)u7-ke+g0aiui
    
    ALLOWED_HOST=127.0.0.1
    
    POSTGRES_HOST=database
    
    POSTGRES_DB=database
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=root
    POSTGRES_PORT=5432
    
    NGINX_EXTERNAL_PORT=80
    NGINX_EXTERNAL_SSL_PORT=443
    
    YOOKASSA_ACCOUNT_ID=<integer>
    YOOKASSA_SECRET_KEY=<string>

Контейнеры запускаются командой

    docker compose up

Авторы:

- Дьяконов Александр (Backend Developer, капитан)
- Тарасов Иван (Backend Developer)
- Мамченко Дмитрий (Frontend Developer, UI/UX Designer)
- деДжофрой Мишель (Frontend Developer, UI/UX Designer)
