import os

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.auth_utils import get_current_user
from app.config import get_settings, Settings
from app.db import get_db
from app.main import create_application
from app.models import Base
from app.schemas import UserCreate


SQLALCHEMY_TEST_DATABASE_URL = 'sqlite:///app_test.db'
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


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield from override_get_db()
    os.remove('app_test.db')


@pytest.fixture(scope='module')
def test_app():
    app = create_application()
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = override_test_settings
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope='session')
def single_user_schema():
    return UserCreate(
        first_name='test1',
        last_name='user1',
        email='test1@user.com',
        password='password')


@pytest.fixture(scope='session')
def three_user_schemas():
    user_one = UserCreate(
        first_name='test1',
        last_name='user1',
        email='test1@user.com',
        password='password')
    user_two = UserCreate(
        first_name='test2',
        last_name='user2',
        email='test2@user.com',
        password='password')
    user_three = UserCreate(
        first_name='test3',
        last_name='user3',
        email='test3@user.com',
        password='password')

    return user_one, user_two, user_three
