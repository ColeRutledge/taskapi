# import json
# from collections import namedtuple
# from typing import Union

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
