from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'FastAPI App'
    admin_email: str = None
    db_url: str = 'sqlite:///app.db'
    secret_key: str = None
    algorithm: str = None
    access_token_expires_minutes: int = None

    class Config:
        env_file = '.env'
