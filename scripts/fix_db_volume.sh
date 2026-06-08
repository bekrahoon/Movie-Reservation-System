#!/usr/bin/env sh
set -e

echo "Stopping docker compose..."
docker compose down || true

VOLUME_NAME="movie_reservation_system_db_data"

echo "Inspecting volume contents (if any):"
docker run --rm -v ${VOLUME_NAME}:/data busybox sh -c "ls -la /data || true"

echo "Attempting to fix ownership inside the volume (may require docker permissions)..."
# UID/GID 999 is the default 'postgres' user in the official image; adjust if needed
docker run --rm -v ${VOLUME_NAME}:/var/lib/postgresql/data --entrypoint sh postgres:latest -c "chown -R 999:999 /var/lib/postgresql/data || true"

echo "If ownership fix failed or you want a clean start, you can remove the volume with:
  docker volume rm ${VOLUME_NAME}
Then bring compose up again:
  docker compose up --build
"

echo "Done."
