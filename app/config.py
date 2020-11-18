from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'FastAPI App'
    admin_email: str = None
    db_url: str = 'sqlite:///app.db'

    class Config:
        env_file = '.env'
