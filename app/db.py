from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings


SQLALCHEMY_DATABASE_URL = get_settings().db_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},  # TODO: remove for prod
)

# configurable session factory for creating Session objs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
