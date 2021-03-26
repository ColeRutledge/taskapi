from datetime import timedelta

from jose import jwt

from app.auth import auth_utils
from app.auth.auth_utils import create_access_token


TEST_SECRET_KEY = 'samplekeyfortests'
TEST_ALGORITHM = 'HS256'


def test_create_access_token(monkeypatch):
    data_to_encode = {'sub': 'test@user.com'}
    expires_in_thirty = timedelta(minutes=30)

    monkeypatch.setattr(auth_utils, 'SECRET_KEY', TEST_SECRET_KEY)
    monkeypatch.setattr(auth_utils, 'ALGORITHM', TEST_ALGORITHM)

    encoded = create_access_token(data_to_encode, expires_delta=expires_in_thirty)
    decoded = jwt.decode(encoded, TEST_SECRET_KEY, TEST_ALGORITHM)

    assert decoded.get('sub') == 'test@user.com'
