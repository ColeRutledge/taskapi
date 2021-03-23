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


def test_get_all_teams(monkeypatch, test_app: TestClient):

    def mock_read_all(*args):
        mock_team1 = models.Team(id=1, team_name='Engineering')
        mock_team2 = models.Team(id=2, team_name='IT')
        return [mock_team1, mock_team2]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/teams/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {'id': 1, 'team_name': 'Engineering'}, {'id': 2, 'team_name': 'IT'}]


@pytest.mark.parametrize(
    argnames=['team_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'team_name', 'Engineering'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Team not found')])
def test_get_team(
        team_id: int,
        status_code: int,
        field: str,
        value: str,
        monkeypatch,
        test_app: TestClient):

    mock_team = models.Team(id=1, team_name='Engineering')

    def mock_read(*args):
        if team_id == 0:  # team that does not exist
            return None
        return mock_team

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/teams/{team_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['team_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 1, {'id': 2, 'project_name': 'Two', 'team_id': 1}),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Team not found')])
def test_get_team_projects(
        team_id: int,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    MockTeamWithProjects = namedtuple('MockTeamWithProjects', ['projects'])
    mock_team = MockTeamWithProjects(projects=[
        models.Project(id=1, project_name='One', team_id=1),
        models.Project(id=2, project_name='Two', team_id=1)])

    def mock_read(*args):
        if team_id == 0:
            return None
        return mock_team

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/teams/{team_id}/projects')
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['team_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 1, {
            'id': 2, 'first_name': 'Test2', 'last_name': 'User2',
            'email': 'test2@user.com', 'team_id': 1, 'disabled': None}),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Team not found')])
def test_get_team_users(
        team_id: int,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    MockTeamWithUsers = namedtuple('MockTeamWithUsers', ['users'])
    mock_team = MockTeamWithUsers(users=[
        models.User(
            id=1, first_name='Test1', last_name='User1',
            email='test1@user.com', team_id=1),
        models.User(
            id=2, first_name='Test2', last_name='User2',
            email='test2@user.com', team_id=1)])

    def mock_read(*args):
        if team_id == 0:
            return None
        return mock_team

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/teams/{team_id}/users')
    assert response.status_code == status_code
    assert response.json()[field] == value


def test_create_team(monkeypatch, test_app: TestClient):

    def mock_create(*args):
        return models.Team(id=1, team_name='Engineering')

    monkeypatch.setattr(crud, 'create', mock_create)
    payload = json.dumps({'team_name': 'Engineering'})
    response = test_app.post('/teams/', data=payload)
    assert response.status_code == HTTP_201_CREATED
    assert response.json() == {'id': 1, 'team_name': 'Engineering'}


@pytest.mark.parametrize(
    argnames=['team_id', 'team_name', 'status_code', 'field', 'value'],
    argvalues=[
        (1, 'Engineering', HTTP_200_OK, 'team_name', 'Engineering'),
        (0, 'Bad Team ID', HTTP_404_NOT_FOUND, 'detail', 'Team not found')])
def test_update_team(
        team_id: int,
        team_name: str,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    def mock_read(*args):
        if team_id == 0:
            return None
        return models.Team(id=team_id, team_name='Pre-Change')

    def mock_update_team(*args):
        return models.Team(id=team_id, team_name=team_name)

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'update_team', mock_update_team)

    payload = json.dumps({'team': {'team_name': team_name}})
    response = test_app.put(f'/teams/{team_id}', data=payload)
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['team_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'team_name', 'Engineering'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Team not found')])
def test_delete_team(
        team_id: int,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    mock_team = models.Team(id=team_id, team_name='Engineering')

    def mock_read(*args):
        if team_id == 0:
            return None
        return mock_team

    def mock_delete(*args):
        return mock_team

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'delete', mock_delete)

    response = test_app.delete(f'/teams/{team_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value
