from app import models


def test_authenticate_user(monkeypatch):
    mock_user = models.User(
        id=1,
        first_name='Test',
        last_name='User',
        email='test@user.com',
        team_id=1,
        hashed_password='password')

    def mock_get_user_by_email(*args, **kwargs):
        return mock_user

    def mock_verify(*args):
        return True

    monkeypatch.setattr(models.User, 'get_user_by_email', mock_get_user_by_email)
    monkeypatch.setattr(models.pwd_context, 'verify', mock_verify)
    user = models.User.authenticate_user('test@user.com', 'password', 'fake_db_session')
    assert isinstance(user, models.User)
    assert user.email == 'test@user.com'


def test_authenticate_user_password_fail(monkeypatch):
    mock_user = models.User(
        id=1,
        first_name='Test',
        last_name='User',
        email='test@user.com',
        team_id=1,
        hashed_password='password')

    def mock_get_user_by_email(*args, **kwargs):
        return mock_user

    def mock_verify(*args):
        return False

    monkeypatch.setattr(models.User, 'get_user_by_email', mock_get_user_by_email)
    monkeypatch.setattr(models.pwd_context, 'verify', mock_verify)
    user = models.User.authenticate_user('test@user.com', 'password', 'fake_db_session')
    assert user is False
