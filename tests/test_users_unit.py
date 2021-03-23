import json
from collections import namedtuple
from typing import Union

import pytest
from fastapi.testclient import TestClient

from app import models, crud


HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_401_UNAUTHORIZED = 401


def test_get_all_users(monkeypatch, test_app: TestClient):

    def mock_read_all(*args):
        mock_user = models.User(
            id=1, team_id=1, first_name='Test',
            last_name='User', email='test@user.com')
        return [mock_user]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/users/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == [{
        'first_name': 'Test', 'last_name': 'User', 'id': 1,
        'email': 'test@user.com', 'team_id': 1, 'disabled': None}]


@pytest.mark.parametrize(
    argnames=['user_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'email', 'expected@email.com'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'User not found')])
def test_get_user(
        user_id: int,
        status_code: int,
        field: Union[str, int],
        value: Union[str, int],
        monkeypatch,
        test_app: TestClient):

    mock_user = models.User(
        id=user_id,
        team_id=1,
        first_name='fill',
        last_name='fill',
        email='expected@email.com')

    def mock_read(*args):
        if user_id == 0:  # user that does not exist
            return None
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/users/{user_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['user_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'team_name', 'Testing'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'User not found')])
def test_get_user_team(
        user_id: int,
        status_code: int,
        field: Union[int, str],
        value: Union[int, str],
        monkeypatch,
        test_app: TestClient):

    MockUserWithTeam = namedtuple('MockUserWithTeam', field_names=['team'])
    mock_user = MockUserWithTeam(team=models.Team(id=1, team_name='Testing'))

    def mock_read(*args):
        if user_id == 0:
            return None
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/users/{user_id}/team')
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['user_id', 'email', 'status_code', 'field', 'value'],
    argvalues=[
        (1, 'before@change.com', HTTP_200_OK, 'email', 'post@change.com'),
        (2, 'fill', HTTP_401_UNAUTHORIZED, 'detail', 'Could not validate credentials'),
        (0, 'bad@id.com', HTTP_404_NOT_FOUND, 'detail', 'User not found')])
def test_update_user(
        user_id: int,
        email: str,
        status_code: int,
        field: Union[str, int],
        value: Union[str, int],
        monkeypatch,
        test_app: TestClient):

    mock_user = models.User(
        id=user_id,
        team_id=1,
        first_name='fill',
        last_name='fill',
        email=email)

    def mock_read(*args):
        if user_id == 0:
            return None
        return mock_user

    def mock_update_user(*args):
        mock_user.email = 'post@change.com'
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'update_user', mock_update_user)

    payload = json.dumps({'user_schema': {'email': email}})
    response = test_app.put(f'/users/{user_id}', data=payload)
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['user_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'id', 1),
        (2, HTTP_401_UNAUTHORIZED, 'detail', 'Could not validate credentials'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'User not found')])
def test_delete_user(
        user_id: int,
        status_code: int,
        field: Union[str, int],
        value: Union[str, int],
        monkeypatch,
        test_app: TestClient):

    mock_user = models.User(
        id=user_id,
        team_id=1,
        first_name='Test',
        last_name='User',
        email='test@user.com')

    def mock_read(*args):
        if user_id == 0:
            return None
        return mock_user

    def mock_delete(*args):
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'delete', mock_delete)

    response = test_app.delete(f'/users/{user_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['email', 'status_code', 'field', 'value'],
    argvalues=[
        ('new@user.com', HTTP_201_CREATED, 'id', 1),
        ('exist@user.com', HTTP_400_BAD_REQUEST, 'detail', 'Email already registered')])
def test_create_user(
        email: str,
        status_code: int,
        field: Union[str, int],
        value: Union[str, int],
        monkeypatch,
        test_app: TestClient):

    mock_user = models.User(
        id=1,
        team_id=1,
        first_name='Test',
        last_name='User',
        email=email)

    def mock_get_user_by_email(*args):
        if email == 'exist@user.com':
            return mock_user
        return None

    def mock_create_user(*args):
        return mock_user

    monkeypatch.setattr(models.User, 'get_user_by_email', mock_get_user_by_email)
    monkeypatch.setattr(crud, 'create_user', mock_create_user)

    payload = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': email,
        'password': 'password'}
    response = test_app.post('/users/', data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()[field] == value
