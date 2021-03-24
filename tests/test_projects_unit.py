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


def test_get_all_projects(monkeypatch, test_app: TestClient):

    def mock_read_all(*args):
        mock_project1 = models.Project(id=1, project_name='Test', team_id=1)
        mock_project2 = models.Project(id=2, project_name='Deploy', team_id=1)
        return [mock_project1, mock_project2]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/projects/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {'id': 1, 'project_name': 'Test', 'team_id': 1},
        {'id': 2, 'project_name': 'Deploy', 'team_id': 1}]


@pytest.mark.parametrize(
    argnames=['project_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'project_name', 'Test'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Project not found')])
def test_get_project(
        project_id: int,
        status_code: int,
        field: str,
        value: str,
        monkeypatch,
        test_app: TestClient):

    mock_project = models.Project(id=1, project_name='Test', team_id=1)

    def mock_read(*args):
        if project_id == 0:  # project that does not exist
            return None
        return mock_project

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/projects/{project_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['project_id', 'status_code', 'fields', 'value'],
    argvalues=[
        (1, HTTP_200_OK, '["project_data"]["Column2"]', [{
            'id': 3, 'task_description': 'task3',
            'column_idx': 0, 'column_id': 2, 'due_date': None}]),
        (0, HTTP_404_NOT_FOUND, '["detail"]', 'Project not found')])
def test_get_project_data(
        project_id: int,
        status_code: int,
        fields: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    mock_project = models.Project(id=1, project_name='Deploy', team_id=1)

    def mock_read(*args):
        if project_id == 0:
            return None
        return mock_project

    def mock_get_project_data(*args):
        return {
            'project_data': {
                'Column1': [
                    models.Task(
                        id=1, task_description='task1',
                        column_idx=0, column_id=1, due_date=None),
                    models.Task(
                        id=2, task_description='task2',
                        column_idx=1, column_id=1, due_date=None)],
                'Column2': [
                    models.Task(
                        id=3, task_description='task3',
                        column_idx=0, column_id=2, due_date=None)]}}

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(models.Project, 'get_project_data', mock_get_project_data)
    response = test_app.get(f'/projects/{project_id}/data')
    assert response.status_code == status_code
    assert eval(f'response.json(){fields}') == value


@pytest.mark.parametrize(
    argnames=['project_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 1, {
            'id': 2, 'column_name': 'Column2', 'column_pos': 1, 'project_id': 1}),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Project not found')])
def test_get_project_columns(
        project_id: int,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    MockProjectWithColumns = namedtuple('MockProjectWithColumns', ['columns'])
    mock_project = MockProjectWithColumns(columns=[
        models.Column(id=1, column_name='Column1', column_pos=0, project_id=1),
        models.Column(id=2, column_name='Column2', column_pos=1, project_id=1)])

    def mock_read(*args):
        if project_id == 0:
            return None
        return mock_project

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/projects/{project_id}/columns')
    assert response.status_code == status_code
    assert response.json()[field] == value


def test_create_project(monkeypatch, test_app: TestClient):

    def mock_create(*args):
        return models.Project(id=1, project_name='UnitTest', team_id=1)

    monkeypatch.setattr(crud, 'create', mock_create)
    payload = json.dumps({'project_name': 'UnitTest', 'team_id': 1})
    response = test_app.post('/projects/', data=payload)
    assert response.status_code == HTTP_201_CREATED
    assert response.json() == {'id': 1, 'project_name': 'UnitTest', 'team_id': 1}


@pytest.mark.parametrize(
    argnames=['project_id', 'project_name', 'status_code', 'field', 'value'],
    argvalues=[
        (1, 'UnitTest', HTTP_200_OK, 'project_name', 'UnitTest'),
        (0, 'BadProjectID', HTTP_404_NOT_FOUND, 'detail', 'Project not found')])
def test_update_project(
        project_id: int,
        project_name: str,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    def mock_read(*args):
        if project_id == 0:
            return None
        return models.Project(id=project_id, project_name='Pre-Change', team_id=1)

    def mock_update_project(*args):
        return models.Project(id=project_id, project_name=project_name, team_id=1)

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'update_project', mock_update_project)

    payload = json.dumps({'project': {'project_name': project_name, 'team_id': 1}})
    response = test_app.put(f'/projects/{project_id}', data=payload)
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['project_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'project_name', 'UnitTest'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Project not found')])
def test_delete_project(
        project_id: int,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    mock_project = models.Project(id=project_id, project_name='UnitTest', team_id=1)

    def mock_read(*args):
        if project_id == 0:
            return None
        return mock_project

    def mock_delete(*args):
        return mock_project

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'delete', mock_delete)

    response = test_app.delete(f'/projects/{project_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value
