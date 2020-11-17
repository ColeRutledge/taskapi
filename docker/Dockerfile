FROM python:3.9

RUN pip install --no-cache-dir uvicorn[standard] gunicorn fastapi

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


#### DOCKER COMMANDS ####

# command to build image setting build context with -f
# docker build -t fastapi -f .\docker\Dockerfile .

# command to start container with image in detached mode. will remove on fail/exit
# docker run -d --rm --name asana_api -p 80:80 fastapi
