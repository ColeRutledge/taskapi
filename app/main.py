from fastapi import FastAPI, Depends
from functools import lru_cache
from sqlalchemy.orm.session import Session
from . import config, models, schemas, crud
from app.db import engine, get_db


@lru_cache()
def get_settings():
    return config.Settings()


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get('/info')
async def info(settings: config.Settings = Depends(get_settings)):
    return {
        'app_name': settings.app_name,
        'admin_email': settings.admin_email,
        'db_url': settings.db_url,
    }
