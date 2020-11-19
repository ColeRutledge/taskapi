from fastapi import FastAPI
from functools import lru_cache
from . import config, models
from app.db import engine
from app.routers import users


@lru_cache()
def get_settings():
    return config.Settings()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(users.router)
