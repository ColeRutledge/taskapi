import json
# from collections import namedtuple
from typing import Union

import pytest
from fastapi.testclient import TestClient

from app import models, crud


HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_401_UNAUTHORIZED = 401


def test_get_all_tasks(monkeypatch, test_app: TestClient):

    def mock_read_all(*args):
        mock_task1 = models.Task(
            id=1, task_description='UnitTest', due_date=None, column_idx=0, column_id=1)
        mock_task2 = models.Task(
            id=2, task_description='SmokeTest', due_date=None, column_idx=1, column_id=1)
        return [mock_task1, mock_task2]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/tasks/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {'id': 1, 'task_description': 'UnitTest',
         'due_date': None, 'column_idx': 0, 'column_id': 1},
        {'id': 2, 'task_description': 'SmokeTest',
         'due_date': None, 'column_idx': 1, 'column_id': 1}]


@pytest.mark.parametrize(
    argnames=['task_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'task_description', 'UnitTest'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Task not found')])
def test_get_task(
        task_id: int,
        status_code: int,
        field: str,
        value: str,
        monkeypatch,
        test_app: TestClient):

    mock_task = models.Task(
        id=1, task_description='UnitTest', due_date=None, column_idx=0, column_id=1)
    # models.Task(
    #     id=2, task_description='SmokeTest', due_date=None, column_idx=1, column_id=1)

    def mock_read(*args):
        if task_id == 0:  # task that does not exist
            return None
        return mock_task

    monkeypatch.setattr(crud, 'read', mock_read)
    response = test_app.get(f'/tasks/{task_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value


def test_create_task(monkeypatch, test_app: TestClient):

    def mock_create(*args):
        return models.Task(id=1, task_description='UnitTest', column_idx=0, column_id=1)

    monkeypatch.setattr(crud, 'create', mock_create)
    payload = json.dumps({
        'task_description': 'UnitTest', 'column_idx': 0, 'column_id': 1})
    response = test_app.post('/tasks/', data=payload)
    assert response.status_code == HTTP_201_CREATED
    assert response.json() == {
        'id': 1, 'task_description': 'UnitTest',
        'due_date': None, 'column_idx': 0, 'column_id': 1}


@pytest.mark.parametrize(
    argnames=['task_id', 'task_description', 'status_code', 'field', 'value'],
    argvalues=[
        (1, 'UnitTest', HTTP_200_OK, 'task_description', 'UnitTest'),
        (0, 'BadTaskID', HTTP_404_NOT_FOUND, 'detail', 'Task not found')])
def test_update_task(
        task_id: int,
        task_description: str,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    mock_task = models.Task(
        id=1,
        task_description='PreChange',
        column_idx=0,
        column_id=1)

    def mock_read(*args):
        if task_id == 0:
            return None
        return mock_task

    def mock_update_task(*args):
        mock_task.task_description = task_description
        return mock_task

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'update_task', mock_update_task)

    payload = json.dumps({'task': {'task_description': task_description}})
    response = test_app.put(f'/tasks/{task_id}', data=payload)
    assert response.status_code == status_code
    assert response.json()[field] == value


@pytest.mark.parametrize(
    argnames=['task_id', 'status_code', 'field', 'value'],
    argvalues=[
        (1, HTTP_200_OK, 'task_description', 'UnitTest'),
        (0, HTTP_404_NOT_FOUND, 'detail', 'Task not found')])
def test_delete_task(
        task_id: int,
        status_code: int,
        field: str,
        value: Union[str, dict],
        monkeypatch,
        test_app: TestClient):

    mock_task = models.Task(id=1, task_description='UnitTest', column_idx=0, column_id=1)

    def mock_read(*args):
        if task_id == 0:
            return None
        return mock_task

    def mock_delete(*args):
        return mock_task

    monkeypatch.setattr(crud, 'read', mock_read)
    monkeypatch.setattr(crud, 'delete', mock_delete)

    response = test_app.delete(f'/tasks/{task_id}')
    assert response.status_code == status_code
    assert response.json()[field] == value
