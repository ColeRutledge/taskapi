from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import auth_utils
from app.auth.auth_utils import (
    create_access_token, get_current_active_user, get_current_user)


TEST_SECRET_KEY = 'samplekeyfortests'
TEST_ALGORITHM = 'HS256'
HTTP_401_UNAUTHORIZED = 401


def test_create_access_token(monkeypatch):
    data_to_encode = {'sub': 'test@user.com'}
    expires_in_thirty = timedelta(minutes=30)

    monkeypatch.setattr(auth_utils, 'SECRET_KEY', TEST_SECRET_KEY)
    monkeypatch.setattr(auth_utils, 'ALGORITHM', TEST_ALGORITHM)

    encoded = create_access_token(data_to_encode, expires_delta=expires_in_thirty)
    decoded = jwt.decode(encoded, TEST_SECRET_KEY, TEST_ALGORITHM)

    assert decoded.get('sub') == 'test@user.com'


def test_get_current_user(monkeypatch, test_db_seeded: Session):
    monkeypatch.setattr(auth_utils, 'SECRET_KEY', TEST_SECRET_KEY)
    monkeypatch.setattr(auth_utils, 'ALGORITHM', TEST_ALGORITHM)

    data_to_encode = {'sub': 'bob@smith.com'}
    token = jwt.encode(data_to_encode, TEST_SECRET_KEY, TEST_ALGORITHM)
    user: models.User = get_current_user(test_db_seeded, token)

    assert user.email == 'bob@smith.com'


@pytest.mark.parametrize(
    argnames=['data_to_encode'],
    argvalues=[[{}], [{'sub': 'doesnt@exist.com'}]])
def test_get_current_user_not_existing(data_to_encode, monkeypatch, test_db: Session):
    monkeypatch.setattr(auth_utils, 'SECRET_KEY', TEST_SECRET_KEY)
    monkeypatch.setattr(auth_utils, 'ALGORITHM', TEST_ALGORITHM)

    token = jwt.encode(data_to_encode, TEST_SECRET_KEY, TEST_ALGORITHM)

    with pytest.raises(HTTPException) as exception:
        get_current_user(test_db, token)

    assert exception.value.detail == 'Could not validate credentials'


def test_get_current_active_user():
    active_user = schemas.User(
        id=1,
        first_name='test',
        last_name='user',
        email='pass',
        team_id=1,
        disabled=False)

    user = get_current_active_user(active_user)
    assert user == active_user


def test_get_current_active_user_disabled():
    disabled_user = schemas.User(
        id=1,
        first_name='test',
        last_name='user',
        email='pass',
        team_id=1,
        disabled=True)

    with pytest.raises(HTTPException) as exception:
        get_current_active_user(disabled_user)

    assert exception.value.detail == 'Inactive user'
