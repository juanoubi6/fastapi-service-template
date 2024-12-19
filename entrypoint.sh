#!/bin/ash
set -e

# Run migrations
echo "Running migrations..."
alembic upgrade head

echo "Starting $@"
exec "$@"