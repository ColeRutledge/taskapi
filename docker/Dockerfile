########
# BASE #
########

FROM python:3.9-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


###########
# Builder #
###########

FROM base as builder

RUN apt-get update \
    && apt-get -y --no-install-recommends install curl build-essential \
    && apt-get clean

ENV POETRY_VERSION=1.1.5
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry install --no-dev


###############
# Development #
###############

FROM base as dev

ENV FASTAPI_ENV=development

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /app
COPY . .
RUN chmod +x ./docker/start-reload.sh

EXPOSE 8000

CMD ["./docker/start-reload.sh"]


##############
# Production #
##############

FROM base as prod

ENV FASTAPI_ENV=production

COPY --from=builder $VENV_PATH $VENV_PATH

WORKDIR /app
COPY . .
RUN chmod +x ./docker/start.sh

RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app .
USER app

EXPOSE 8000

CMD ["./docker/start.sh"]
