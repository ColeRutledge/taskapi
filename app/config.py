from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'FastAPI App'
    admin_email: str = None

    class Config:
        env_file = '.env'
