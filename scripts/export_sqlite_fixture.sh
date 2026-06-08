#!/usr/bin/env sh
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

if [ ! -f "db.sqlite3" ]; then
  echo "db.sqlite3 not found in project root. Ensure you're in the project directory where SQLite DB is located."
  exit 1
fi

echo "Exporting data from SQLite to data.json (excluding contenttypes and auth.permission)..."
.
# Use the project's virtualenv if present
if [ -f ".venv/bin/activate" ]; then
  . .venv/bin/activate
fi

# Ensure settings use local SQLite when exporting
export USE_SQLITE=True

python manage.py dumpdata --natural-primary --natural-foreign \
  --exclude contenttypes \
  --exclude auth.permission \
  --exclude authtoken \
  --exclude sessions \
  --exclude admin.logentry \
  --indent 2 > data.json

echo "Export complete: $PROJECT_DIR/data.json"
