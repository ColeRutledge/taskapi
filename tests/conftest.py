from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import get_db
from app.main import create_application
from app.models import Base
from app.config import get_settings, Settings


SQLALCHEMY_TEST_DATABASE_URL = 'sqlite:///app_test.db'
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={'check_same_thread': False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_test_settings():
    return Settings(db_url=SQLALCHEMY_TEST_DATABASE_URL)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module')
def test_app():
    app = create_application()
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_settings] = override_test_settings
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
