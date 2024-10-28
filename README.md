# Movie-Reservation-System

https://roadmap.sh/projects/movie-reservation-system

Table of  Contents:
====================
- [Movie-Reservation-System](#movie-reservation-system)
- [Table of  Contents:](#table-of--contents)
- [Movie Reservation System](#movie-reservation-system-1)
  - [Описание](#описание)
  - [Установка](#установка)
  - [Docker](#docker)




# Movie Reservation System

## Описание
Система бронирования фильмов, позволяющая пользователям бронировать билеты на фильмы и оплачивать их онлайн. Поддерживает создание учетных записей пользователей, авторизацию и корзину для удобного бронирования нескольких билетов.

## Установка

1. Клонируйте репозиторий:
   ```sh
   git clone https://github.com/bekrahoon/Movie-Reservation-System.git

2. Перейдите в директорию проекта:
    ```sh
    cd Movie-Reservation-System

3. Настройте файл `.env` с вашими переменными окружения:

    ```plaintext
    DEBUG = True
    ALLOWED_HOSTS = "*"
    SECRET_KEY = your_SECRET_KEY
    DATABASE_NAME = your_DATABASE_NAME
    DATABASE_USER = your_DATABASE_USER
    DATABASE_PASSWORD = your_DATABASE_PASSWORD

## Docker

1. Создайте и запустите контейнеры:
    ```sh
    docker-compose up --build

2. Выполните миграции базы данных:
    ```sh 
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate

3. Создайте суперпользователя:
    ```sh
    docker-compose exec web python manage.py createsuperuser

4. Перейдите по адресу http://localhost:8000 для доступа к приложению.

