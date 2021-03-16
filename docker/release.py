#! /usr/bin/env python3

# from urllib import request

import os
import subprocess

print(os.environ.get('HEROKU_AUTH'))
print(os.environ)

WEB_DOCKER_IMAGE_ID = subprocess.run([
    'docker',
    'inspect',
    'registry.heroku.com/asana-fastapi/web:latest',
    '--format={{.Id}}'], capture_output=True, encoding='utf-8').stdout

print(WEB_DOCKER_IMAGE_ID)

data = {"updates": [{"type": "web", "docker_image": f"{WEB_DOCKER_IMAGE_ID}"}]}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.heroku+json; version=3.docker-releases"}

# req = request.Request(
#     url='https://api.heroku.com/apps/asana-fastapi/formation',
#     data=data,
#     method='PATCH',
#     headers=headers)

# print(req)

# curl --netrc -X PATCH https://api.heroku.com/apps/$APP_ID_OR_NAME/formation \
#   -d '{
#   "updates": [
#     {
#       "type": "web",
#       "docker_image": "$WEB_DOCKER_IMAGE_ID"
#     },
#     {
#       "type": "worker",
#       "docker_image": "$WORKER_DOCKER_IMAGE_ID"
#     }
#   ]
# }' \
#   -H "Content-Type: application/json" \
#   -H "Accept: application/vnd.heroku+json; version=3.docker-releases"
