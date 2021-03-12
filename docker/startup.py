#!/usr/bin/env python3

import os
import subprocess

from pathlib import Path


print('***** STARTUP inside startup.py *****')


if Path('/app/app/main.py').exists():
    DEFAULT_MODULE_NAME = 'app.main'
elif Path('/app/main.py').exists():
    DEFAULT_MODULE_NAME = 'main'

MODULE_NAME = DEFAULT_MODULE_NAME
VARIABLE_NAME = 'app'

os.environ['APP_MODULE'] = f'{MODULE_NAME}:{VARIABLE_NAME}'

if Path('/app/gunicorn_conf.py').exists():
    DEFAULT_GUNICORN_CONF = '/app/gunicorn_conf.py'
elif Path('/app/app/gunicorn_conf.py').exists():
    DEFAULT_GUNICORN_CONF = '/app/app/gunicorn_conf.py'
elif Path('/app/docker/gunicorn_conf.py').exists():
    DEFAULT_GUNICORN_CONF = '/app/docker/gunicorn_conf.py'
else:
    DEFAULT_GUNICORN_CONF = '/gunicorn_conf.py'

os.environ['GUNICORN_CONF'] = DEFAULT_GUNICORN_CONF
os.environ['WORKER_CLASS'] = 'uvicorn.workers.UvicornWorker'

prestart_script = '/app/app/prestart.sh'

if Path(prestart_script).exists():
    print('Running script prestart.sh')
    subprocess.run([f'{prestart_script}'])
else:
    print('There is no script prestart.sh')

subprocess.run(
    ['gunicorn',
     '-k', os.environ.get('WORKER_CLASS'),
     '-c', os.environ.get('GUNICORN_CONF'),
     os.environ.get('APP_MODULE'),
     '--forwarded-allow-ips', '*']
)
