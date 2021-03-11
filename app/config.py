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
