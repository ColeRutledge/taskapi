import os
from typing import Optional

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


def create_database_engine(database_url: Optional[str] = None):
    SQLALCHEMY_DATABASE_URL = (
        database_url
        if database_url is not None
        else get_settings().db_url
    )

    if database_url is not None:
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args=(
                {'check_same_thread': False}
                if SQLALCHEMY_DATABASE_URL.startswith('sqlite')
                else {}
            ))
    elif os.getenv('FASTAPI_ENV'):        # check if running in container
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
    else:
        engine = create_engine(
            'sqlite:///app.db',
            connect_args={'check_same_thread': False})

    if engine.dialect.name == 'sqlite':
        event.listen(engine, 'connect', _enable_sqlite_foreign_keys)

    return engine


def _enable_sqlite_foreign_keys(connection, record):
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=create_database_engine())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
