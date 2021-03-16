#! /usr/bin/env python3

# from urllib import request, parse, error
import requests

import os
import subprocess

HEROKU_AUTH_TOKEN = os.environ.get('HEROKU_AUTH')
WEB_DOCKER_IMAGE_ID = subprocess.run([
    'docker',
    'inspect',
    'registry.heroku.com/asana-fastapi/web:latest',
    '--format={{.Id}}'], capture_output=True, encoding='utf-8').stdout.strip()

data = {"updates": [{"type": "web", "docker_image": f"{WEB_DOCKER_IMAGE_ID}"}]}
# data = parse.urlencode(data)
# data = data.encode('ascii')
headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.heroku+json; version=3.docker-releases",
    "Authorization": f"Bearer {HEROKU_AUTH_TOKEN}"}


r = requests.patch(
    data=data,
    headers=headers,
    url="https://api.heroku.com/apps/asana-fastapi/formation")

print(r)

# res = request.Request(
#     url="https://api.heroku.com/apps/asana-fastapi/formation",
#     data=data,
#     method='PATCH',
#     headers=headers)

# try:
#     with request.urlopen(res) as response:
#         html = response.read().decode('utf-8')
#         print(html)
# except error.HTTPError as e:
#     print(e.reason)
