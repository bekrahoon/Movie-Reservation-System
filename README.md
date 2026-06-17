# Movie-Reservation-System

https://roadmap.sh/projects/movie-reservation-system

Table of  Contents:
====================
- [Movie-Reservation-System](#movie-reservation-system)
- [Table of  Contents:](#table-of--contents)
- [Movie Reservation System](#movie-reservation-system-1)
  - [Description](#description)
  - [Installation](#installation)
  - [Docker](#docker)



# Movie Reservation System
![image-logo](static/img/screen.png)

## Description
A movie booking system that allows users to book movie tickets and pay online. Supports user account creation, authorization and shopping cart for easy booking of multiple tickets.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/bekrahoon/Movie-Reservation-System.git

2. Navigate to the project directory:
    ```sh
    cd Movie-Reservation-System

3. Customize the `.env` file with your environment variables:

    ```plaintext
    DEBUG = True
    ALLOWED_HOSTS = "*"
    SECRET_KEY = your_SECRET_KEY
    DATABASE_NAME = your_DATABASE_NAME
    DATABASE_USER = your_DATABASE_USER
    DATABASE_PASSWORD = your_DATABASE_PASSWORD

## Docker

1. Create and run containers:
    ```sh
    docker-compose up --build

2. Perform database migrations:
    ```sh 
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate

3. Create a superuser:
    ```sh
    docker-compose exec web python manage.py createsuperuser

4. Go to http://localhost:8000 to access the application.

## Troubleshooting PostgreSQL container

If the `db` container becomes `unhealthy` or exits with code 1, common fixes:

- View logs:
    ```sh
    docker compose logs db --tail 200 --follow
    ```
- Inspect container state:
    ```sh
    docker compose ps
    docker inspect movie_reservation_system-db-1
    ```
- Check volume contents and ownership (this may require sudo/docker privileges):
    ```sh
    ./scripts/fix_db_volume.sh
    # or manually:
    docker run --rm -v movie_reservation_system_db_data:/var/lib/postgresql/data busybox sh -c "ls -la /var/lib/postgresql/data || true"
    ```
- If volume permissions are wrong you can either chown inside the volume or remove the volume (will delete DB data):
    ```sh
    docker run --rm -v movie_reservation_system_db_data:/var/lib/postgresql/data --entrypoint sh postgres:latest -c "chown -R 999:999 /var/lib/postgresql/data || true"
    docker compose down
    docker volume rm movie_reservation_system_db_data
    docker compose up --build
    ```

If you want, запустите команды локально и пришлите вывод логов — я помогу проанализировать их дальше.
If port 8000 is already used on your machine (for example by the local dev server), Compose will fail with "bind: address already in use". Two options:

- Stop the process using port 8000 (e.g., your local Django runserver) or kill it:
    ```sh
    # find and kill the process (Linux/macOS)
    lsof -i :8000
    kill <PID>
    ```
- Or run the containers on a different host port by setting `HOST_PORT` in your `.env` or environment. Example to use 8001:
    ```sh
    # in project root
    export HOST_PORT=8001
    docker compose up --build
    ```

## Telegram Mini App

Проект поддерживает вход через Telegram Mini App. Пользователи могут связать Telegram-аккаунт с аккаунтом на сайте через номер телефона.

### Настройка

1. Создайте бота у [@BotFather](https://t.me/BotFather) и получите токен.

2. Добавьте токен в `.env`:
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   ```

3. Настройте Mini App в @BotFather:
   - Откройте @BotFather → `/mybots` → выберите бота → **Bot Settings** → **Menu Button**.
   - Или: `/newapp` → укажите URL: `https://your-domain.com/telegram/`.

4. Пересоберите контейнеры:
   ```sh
   docker-compose up --build
   ```

### Как это работает

- Пользователь открывает Mini App в Telegram.
- Бэкенд проверяет подпись `initData` (HMAC-SHA256) — без серверной проверки вход невозможен.
- Если `telegram_id` уже привязан к аккаунту — автоматический вход.
- Если нет — Telegram запрашивает контакт. По номеру телефона ищется существующий аккаунт на сайте:
  - Найден → привязывается `telegram_id`, вход.
  - Не найден → создаётся новый аккаунт.

### Привязка телефона на сайте

Залогиненные пользователи могут привязать номер телефона на странице `/profile/phone/`. Это позволит связать аккаунт на сайте с Telegram.

### Тестирование локально

Для тестирования Mini App локально используйте [ngrok](https://ngrok.com/) или аналог:
```sh
ngrok http 8000
```
Затем укажите полученный HTTPS-URL в настройках Mini App у @BotFather.

---

### Перенос данных из локальной SQLite в PostgreSQL (Compose)

Если вы работали локально с `db.sqlite3` и хотите перенести таблицы и данные в PostgreSQL (контейнер `db`), выполните:

1. Экспорт данных из SQLite в JSON-фикстуру (на хосте):
```sh
chmod +x scripts/export_sqlite_fixture.sh
./scripts/export_sqlite_fixture.sh
```

2. Запустите Compose (если ещё не запущен):
```sh
export HOST_PORT=8001
docker compose up -d
```

3. Импортируйте фикстуру в Django, запущенный в контейнере `web`:
```sh
chmod +x scripts/import_fixture_to_postgres.sh
./scripts/import_fixture_to_postgres.sh
```

Примечания:
- Скрипт `export_sqlite_fixture.sh` создаёт `data.json` в корне проекта и исключает `contenttypes` и `auth.permission`, чтобы избежать конфликтов при загрузке.
- Перед импортом убедитесь, что миграции применены в контейнере (entrypoint в `web` уже запускает `migrate`).
- После импорта проверьте в админке, что пользователи, модели и записи перенеслись корректно.

