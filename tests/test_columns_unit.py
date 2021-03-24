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


def test_get_all_columns(monkeypatch, test_app: TestClient):

    def mock_read_all(*args):
        mock_col1 = models.Column(id=1, column_name='Test', column_pos=0, project_id=1)
        mock_col2 = models.Column(id=2, column_name='Deploy', column_pos=1, project_id=1)
        return [mock_col1, mock_col2]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/columns/')
    assert response.status_code == HTTP_200_OK
    assert response.json() == [
        {'id': 1, 'column_name': 'Test', 'column_pos': 0, 'project_id': 1},
        {'id': 2, 'column_name': 'Deploy', 'column_pos': 1, 'project_id': 1}]


# @pytest.mark.parametrize(
#     argnames=['column_id', 'status_code', 'field', 'value'],
#     argvalues=[
#         (1, HTTP_200_OK, 'column_name', 'Test'),
#         (0, HTTP_404_NOT_FOUND, 'detail', 'column not found')])
# def test_get_column(
#         column_id: int,
#         status_code: int,
#         field: str,
#         value: str,
#         monkeypatch,
#         test_app: TestClient):

#     mock_column = models.Column(id=1, column_name='Test', project_id=1)

#     def mock_read(*args):
#         if column_id == 0:  # column that does not exist
#             return None
#         return mock_column

#     monkeypatch.setattr(crud, 'read', mock_read)
#     response = test_app.get(f'/columns/{column_id}')
#     assert response.status_code == status_code
#     assert response.json()[field] == value


# @pytest.mark.parametrize(
#     argnames=['column_id', 'status_code', 'fields', 'value'],
#     argvalues=[
#         (1, HTTP_200_OK, '["column_data"]["Column2"]', [{
#             'id': 3, 'task_description': 'task3',
#             'column_idx': 0, 'column_id': 2, 'due_date': None}]),
#         (0, HTTP_404_NOT_FOUND, '["detail"]', 'column not found')])
# def test_get_column_data(
#         column_id: int,
#         status_code: int,
#         fields: str,
#         value: Union[str, dict],
#         monkeypatch,
#         test_app: TestClient):

#     mock_column = models.Column(id=1, column_name='Deploy', project_id=1)

#     def mock_read(*args):
#         if column_id == 0:
#             return None
#         return mock_column

#     def mock_get_column_data(*args):
#         return {
#             'column_data': {
#                 'Column1': [
#                     models.Task(
#                         id=1, task_description='task1',
#                         column_idx=0, column_id=1, due_date=None),
#                     models.Task(
#                         id=2, task_description='task2',
#                         column_idx=1, column_id=1, due_date=None)],
#                 'Column2': [
#                     models.Task(
#                         id=3, task_description='task3',
#                         column_idx=0, column_id=2, due_date=None)]}}

#     monkeypatch.setattr(crud, 'read', mock_read)
#     monkeypatch.setattr(models.Column, 'get_column_data', mock_get_column_data)
#     response = test_app.get(f'/columns/{column_id}/data')
#     assert response.status_code == status_code
#     assert eval(f'response.json(){fields}') == value


# @pytest.mark.parametrize(
#     argnames=['column_id', 'status_code', 'field', 'value'],
#     argvalues=[
#         (1, HTTP_200_OK, 1, {
#             'id': 2, 'column_name': 'Column2', 'column_pos': 1, 'column_id': 1}),
#         (0, HTTP_404_NOT_FOUND, 'detail', 'column not found')])
# def test_get_column_columns(
#         column_id: int,
#         status_code: int,
#         field: str,
#         value: Union[str, dict],
#         monkeypatch,
#         test_app: TestClient):

#     MockcolumnWithColumns = namedtuple('MockcolumnWithColumns', ['columns'])
#     mock_column = MockcolumnWithColumns(columns=[
#         models.Column(id=1, column_name='Column1', column_pos=0, column_id=1),
#         models.Column(id=2, column_name='Column2', column_pos=1, column_id=1)])

#     def mock_read(*args):
#         if column_id == 0:
#             return None
#         return mock_column

#     monkeypatch.setattr(crud, 'read', mock_read)
#     response = test_app.get(f'/columns/{column_id}/columns')
#     assert response.status_code == status_code
#     assert response.json()[field] == value


# def test_create_column(monkeypatch, test_app: TestClient):

#     def mock_create(*args):
#         return models.Column(id=1, column_name='UnitTest', project_id=1)

#     monkeypatch.setattr(crud, 'create', mock_create)
#     payload = json.dumps({'column_name': 'UnitTest', 'project_id': 1})
#     response = test_app.post('/columns/', data=payload)
#     assert response.status_code == HTTP_201_CREATED
#     assert response.json() == {'id': 1, 'column_name': 'UnitTest', 'project_id': 1}


# @pytest.mark.parametrize(
#     argnames=['column_id', 'column_name', 'status_code', 'field', 'value'],
#     argvalues=[
#         (1, 'UnitTest', HTTP_200_OK, 'column_name', 'UnitTest'),
#         (0, 'BadcolumnID', HTTP_404_NOT_FOUND, 'detail', 'column not found')])
# def test_update_column(
#         column_id: int,
#         column_name: str,
#         status_code: int,
#         field: str,
#         value: Union[str, dict],
#         monkeypatch,
#         test_app: TestClient):

#     def mock_read(*args):
#         if column_id == 0:
#             return None
#         return models.Column(id=column_id, column_name='Pre-Change', project_id=1)

#     def mock_update_column(*args):
#         return models.Column(id=column_id, column_name=column_name, project_id=1)

#     monkeypatch.setattr(crud, 'read', mock_read)
#     monkeypatch.setattr(crud, 'update_column', mock_update_column)

#     payload = json.dumps({'column': {'column_name': column_name, 'project_id': 1}})
#     response = test_app.put(f'/columns/{column_id}', data=payload)
#     assert response.status_code == status_code
#     assert response.json()[field] == value


# @pytest.mark.parametrize(
#     argnames=['column_id', 'status_code', 'field', 'value'],
#     argvalues=[
#         (1, HTTP_200_OK, 'column_name', 'UnitTest'),
#         (0, HTTP_404_NOT_FOUND, 'detail', 'column not found')])
# def test_delete_column(
#         column_id: int,
#         status_code: int,
#         field: str,
#         value: Union[str, dict],
#         monkeypatch,
#         test_app: TestClient):

#     mock_column = models.Column(id=column_id, column_name='UnitTest', project_id=1)

#     def mock_read(*args):
#         if column_id == 0:
#             return None
#         return mock_column

#     def mock_delete(*args):
#         return mock_column

#     monkeypatch.setattr(crud, 'read', mock_read)
#     monkeypatch.setattr(crud, 'delete', mock_delete)

#     response = test_app.delete(f'/columns/{column_id}')
#     assert response.status_code == status_code
#     assert response.json()[field] == value
