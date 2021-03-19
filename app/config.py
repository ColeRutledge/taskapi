from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'FastAPI App'
    admin_email: str = None
    db_url: str = 'sqlite:///app.db'
    secret_key: str = 'defaultkeytoreplaceforprod'
    algorithm: str = 'HS256'
    access_token_expires_minutes: int = 30

    class Config:
        env_file = '.env'


@lru_cache()
def get_settings():
    return Settings()


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'fmt': {
            'datefmt': '%H:%M:%S %m-%d-%y',
            'format': '%(asctime)s %(levelname)s %(module)s.'
                      '%(funcName)s[%(lineno)d] %(message)s'}},
    'handlers': {
        'rfh': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/debug.log',
            'maxBytes': 1024 * 1024,  # 1MB
            'encoding': 'utf-8',
            'formatter': 'fmt',
            'backupCount': 2,
            'level': 'INFO',
            'mode': 'a',
            'delay': 0}},
    'loggers': {
        '': {  # root
            'handlers': ['rfh'],
            'level': 'INFO'}}}
