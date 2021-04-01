import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


def create_database_engine():
    SQLALCHEMY_DATABASE_URL = get_settings().db_url

    if os.getenv('FASTAPI_ENV'):        # check if running in container
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
    else:
        engine = create_engine(
            'sqlite:///app.db',
            connect_args={'check_same_thread': False})
    return engine


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=create_database_engine())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
