from fastapi import FastAPI, Depends
from functools import lru_cache
from . import config


@lru_cache()
def get_settings():
    return config.Settings()


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/info')
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'db_url': settings.db_url,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
