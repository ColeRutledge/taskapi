#! /usr/bin/env python3

import json
import os
import subprocess
from urllib import request, error

HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')
HEROKU_AUTH_TOKEN = os.environ.get('HEROKU_AUTH_TOKEN')
WEB_DOCKER_IMAGE_ID = subprocess.run([
    'docker',
    'inspect',
    f'registry.heroku.com/{HEROKU_APP_NAME}/web:latest',
    '--format={{.Id}}'], capture_output=True, encoding='utf-8').stdout.strip()

data = {
    "updates": [{"type": "web", "docker_image": f"{WEB_DOCKER_IMAGE_ID}"}]}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.heroku+json; version=3.docker-releases",
    "Authorization": f"Bearer {HEROKU_AUTH_TOKEN}"}

r = request.Request(
    url=f"https://api.heroku.com/apps/{HEROKU_APP_NAME}/formation",
    data=json.dumps(data).encode('utf-8'),
    method='PATCH',
    headers=headers)

try:
    with request.urlopen(r) as response:
        html = response.read().decode('utf-8')
        print(html)
except error.HTTPError as e:
    raise SystemExit(f'Error with request: {e.reason}')
