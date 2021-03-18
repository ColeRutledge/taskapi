from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.auth.auth_utils import get_current_user
from app.config import get_settings, Settings
from app.db import get_db
from app.main import create_application
from app.models import Base
from tests.seed import seed_db


SQLALCHEMY_TEST_DATABASE_URL = 'sqlite:///app_test.db'
# SQLALCHEMY_TEST_DATABASE_URL = 'sqlite://'
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={'check_same_thread': False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_test_settings():
    return Settings(db_url=SQLALCHEMY_TEST_DATABASE_URL)


def override_get_current_user():
    return True  # could return a User


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module')
def test_app():
    app = create_application()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = override_test_settings
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_db_empty():
    Base.metadata.create_all(bind=engine, checkfirst=True)
    yield from override_get_db()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db_seeded():
    Base.metadata.create_all(bind=engine, checkfirst=True)
    db_session = Session(autocommit=False, autoflush=False, bind=engine)
    seed_db(db_session)
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)
