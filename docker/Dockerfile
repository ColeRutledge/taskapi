#### DOCKER COMMANDS ####

# command to build image setting build context with -f
# docker build -t fastapi -f .\docker\Dockerfile .

# command to start container with image in detached mode. will remove on fail/exit
# docker run -d --rm --name asana_api -p 80:80 fastapi

# FROM python:3.6 as base
# COPY requirements.txt /
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


# FROM python:3.6-alpine
# COPY --from=base /wheels /wheels
# COPY --from=base requirements.txt .
# RUN pip install --no-cache /wheels/* # flask, gunicorn, pycrypto
# WORKDIR /app
# COPY . /app


FROM python:3.9


# some of the additional packages required if using a slim build
# RUN apt-get update && apt-get install curl -y && apt-get install gcc -y

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* ./
RUN poetry install --no-root --no-dev

COPY ./docker/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./docker/gunicorn_conf.py /gunicorn_conf.py

COPY ./docker/start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
