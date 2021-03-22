from collections import namedtuple
import json
from typing import Union

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import models, crud


HTTP_200_OK = status.HTTP_200_OK
HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
HTTP_401_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED


def test_get_all_users(monkeypatch, test_app: TestClient):

    def mock_read_all(db, user_model):
        mock_user = models.User(
            id=1, team_id=1, first_name='Bob',
            last_name='Smith', email='bob@smith.com')
        return [mock_user]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/users/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == [{
        'first_name': 'Bob', 'last_name': 'Smith', 'id': 1,
        'email': 'bob@smith.com', 'team_id': 1, 'disabled': None}]


@pytest.mark.parametrize(
    argnames=['user_id', 'mock_user', 'status_code', 'expected_response'],
    argvalues=[
        (1, models.User(
            id=1, team_id=1, first_name='Bob',
            last_name='Smith', email='bob@smith.com'), HTTP_200_OK, {
                'first_name': 'Bob', 'last_name': 'Smith', 'id': 1,
                'email': 'bob@smith.com', 'team_id': 1, 'disabled': None}),
        (0, None, HTTP_404_NOT_FOUND, {'detail': 'User not found'})])
def test_get_user(
        user_id: int,
        mock_user: models.User,
        status_code: int,
        expected_response: dict,
        monkeypatch,
        test_app: TestClient):

    def mock_read(db, user_id, user_model):
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/users/{user_id}')
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    argnames=['user_id', 'mock_team', 'status_code', 'expected_response'],
    argvalues=[
        (1, {'id': 1, 'team_name': 'Marketing'}, HTTP_200_OK, {
            'id': 1, 'team_name': 'Marketing'}),
        (0, None, HTTP_404_NOT_FOUND, {'detail': 'User not found'})])
def test_get_user_team(
        user_id: int,
        mock_team: models.Team,
        status_code: int,
        expected_response: dict,
        monkeypatch,
        test_app: TestClient):

    def mock_read(db, user_id, user_model):
        mockUserWithTeam = namedtuple('mockUserWithTeam', field_names=['team'])
        mock_user = mockUserWithTeam(team=models.Team(**mock_team)) \
            if mock_team is not None else None
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/users/{user_id}/team')
    assert response.status_code == status_code
    assert response.json() == expected_response


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

    def mock_read(db, uid, user_model):
        if user_id == 0:  # user that does not exist
            return None
        return mock_user

    def mock_update_user(db, user_schema, db_user):
        mock_user.email = 'post@change.com'
        return mock_user

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'update_user', mock_update_user)
    payload = json.dumps({'user_schema': {'email': email}})
    response = test_app.put(f'/users/{user_id}', data=payload)
    assert response.status_code == status_code
    assert response.json()[field] == value
