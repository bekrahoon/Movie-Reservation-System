#!/usr/bin/env sh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

if [ ! -f "data.json" ]; then
  echo "data.json not found — run scripts/export_sqlite_fixture.sh first to create it."
  exit 1
fi

echo "Ensure docker compose is running with the db and web services."
echo "Loading fixture into Django running in container..."

# Copy not required if project is bind-mounted; data.json sits in /app inside container
docker compose exec web python manage.py loaddata /app/data.json

echo "Import complete. Check container logs for errors."
