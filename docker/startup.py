#!/usr/bin/env python3

import subprocess


APP_MODULE = 'app.main:app'
GUNICORN_CONF = '/app/docker/gunicorn_conf.py'
WORKER_CLASS = 'uvicorn.workers.UvicornWorker'

print(f"{' STARTUP ':*^25}")

print(f"{' RUNNING MIGRATIONS ':*^25}")
subprocess.run(['alembic', '-c', 'migrations/alembic.ini', 'upgrade', 'head'])

print(f"{' STARTING SERVER ':*^25}")
subprocess.run([
    'gunicorn',
    '-k', WORKER_CLASS,
    '-c', GUNICORN_CONF,
    '--forwarded-allow-ips', '*',
    APP_MODULE,
])


# #### replaced start.sh #####

# #! /usr/bin/env sh
# set -e

# # activate virtual env
# . /opt/pysetup/.venv/bin/activate

# if [ -f /app/app/main.py ]; then
#     DEFAULT_MODULE_NAME=app.main
# elif [ -f /app/main.py ]; then
#     DEFAULT_MODULE_NAME=main
# fi

# MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
# VARIABLE_NAME=${VARIABLE_NAME:-app}

# export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

# if [ -f /app/gunicorn_conf.py ]; then
#     DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
# elif [ -f /app/app/gunicorn_conf.py ]; then
#     DEFAULT_GUNICORN_CONF=/app/app/gunicorn_conf.py
# elif [ -f /app/docker/gunicorn_conf.py ]; then              # added
#     DEFAULT_GUNICORN_CONF=/app/docker/gunicorn_conf.py
# else
#     DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
# fi

# export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
# export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# # If there's a prestart.sh script in the /app directory or other path specified, run it before starting
# PRE_START_PATH=${PRE_START_PATH:-/app/app/prestart.sh}

# echo "Checking for script in $PRE_START_PATH"
# if [ -f $PRE_START_PATH ] ; then
#     echo "Running script $PRE_START_PATH"
#     . "$PRE_START_PATH"
# else
#     echo "There is no script $PRE_START_PATH"
# fi

# # Start Gunicorn -- TODO: REMOVE --forwarded-allow-ips after adding TLS proxy
# exec gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE" --forwarded-allow-ips "*"
