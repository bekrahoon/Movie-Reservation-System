#!/usr/bin/env sh
set -e
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

export HOST_PORT=${HOST_PORT:-8001}

echo "Building web image..."
docker compose build --no-cache --progress=plain web

echo "Starting services..."
docker compose up -d

db_container=$(docker compose ps -q db)
echo "Waiting for DB ($db_container) to be healthy..."
until [ "$(docker inspect -f '{{.State.Health.Status}}' "$db_container" 2>/dev/null)" = "healthy" ]; do
  sleep 1
done

echo "DB healthy — applying migrations in web..."
docker compose exec web python manage.py migrate --noinput

if [ -f data.json ]; then
  echo "data.json found — loading fixture into web..."
  docker compose exec web python manage.py loaddata /app/data.json
fi

echo "Done. Showing last logs:"
docker compose logs --tail 200