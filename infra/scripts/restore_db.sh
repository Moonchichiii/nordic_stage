#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: ./restore_db.sh <path_to_backup.sql>"
  exit 1
fi

BACKUP_FILE="$1"

# Go to the directory containing docker-compose.yml
cd "$(dirname "$0")/../docker"

echo "Restoring database from $BACKUP_FILE..."
# Drop and recreate the DB to ensure a clean slate, then restore
docker compose exec -T db psql -U postgres -c "DROP DATABASE IF EXISTS nordic_stage;"
docker compose exec -T db psql -U postgres -c "CREATE DATABASE nordic_stage;"
cat "../../$BACKUP_FILE" | docker compose exec -T db psql -U postgres -d nordic_stage

echo "Restore complete!"