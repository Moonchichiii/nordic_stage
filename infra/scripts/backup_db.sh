#!/bin/bash
set -e

# Go to the directory containing docker-compose.yml
cd "$(dirname "$0")/../docker"

BACKUP_DIR="../../backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

echo "Backing up Postgres database..."
# Use -T to disable pseudo-TTY allocation for script compatibility
docker compose exec -T db pg_dump -U postgres -d nordic_stage > "$FILE"

echo "Backup saved to: $FILE"