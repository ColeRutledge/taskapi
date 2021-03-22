# import json
# from collections import namedtuple
# from typing import Union

# import pytest
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
