#! /usr/bin/env bash
#! /usr/bin/env sh      # original

echo "**************** PRESTART ****************"
echo "Running alembic migrations..."
alembic -c migrations/alembic.ini upgrade head
