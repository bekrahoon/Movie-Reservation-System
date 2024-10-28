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
    SECRET_KEY=ваш_секретный_ключ
    STRIPE_SECRET_KEY=ваш_секретный_ключ_Stripe
    STRIPE_PUBLIC_KEY=ваш_публичный_ключ_Stripe
    DATABASE_NAME=имя_базы_данных
    DATABASE_USER=пользователь_базы_данных
    DATABASE_PASSWORD=пароль_базы_данных
    DEBUG=True
    ALLOWED_HOSTS=*

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

