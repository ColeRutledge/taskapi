#! /bin/sh

set -e

IMAGE_ID=$(docker inspect registry.heroku.com/asana-fastapi/web:latest --format={{.Id}})
PAYLOAD='{"updates": [{"type": "web", "docker_image": "'"$IMAGE_ID"'"}]}'

curl -n -X PATCH https://api.heroku.com/apps/asana-fastapi/formation \
    -d "${PAYLOAD}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
    -H "Authorization: Bearer ${HEROKU_AUTH_TOKEN}"
