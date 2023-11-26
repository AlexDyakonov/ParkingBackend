Данный репозиторий является частью проекта, направленного на решение задачи хакатона "Урбатон" по треку "Оптимизация парковочных мест"

Необходимо создать .env файл, который состоит из:

    DJANGO_SECRET_KEY=секретный django ключ
    ALLOWED_HOST=127.0.0.1
    # Если не указывать POSTGRES конфиги, будет использована sqlite
    POSTGRES_HOST=db_host #database при запуске с docker
    POSTGRES_DB=db_name #database при запуске с docker
    POSTGRES_USER=db_username
    POSTGRES_PASSWORD=db_pass
    POSTGRES_PORT=db_port
    NGINX_EXTERNAL_PORT=80
    NGINX_EXTERNAL_SSL_PORT=443
    YOOKASSA_ACCOUNT_ID=
    YOOKASSA_SECRET_KEY=

Для запуска в докере необходимо создать .env.docker

Авторы:
- Дьяконов Александр (Backend Developer, капитан)
- Тарасов Иван (Backend Developer)
- Дьяконов Николай (Backend Developer, analysis of algorithms)
- Мамченко Дмитрий (Frontend Developer, UI/UX Designer)
- деДжофрой Мишель (Frontend Developer, UI/UX Designer)
