import json

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_all_users_returns_all_users(test_app: TestClient, test_db_seeded: Session):
    response = test_app.get('/users/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob@smith.com',
         'id': 1, 'team_id': 1, 'disabled': None},
        {'first_name': 'Sally', 'last_name': 'McBeth', 'email': 'Sally@123.com',
         'id': 2, 'team_id': 1, 'disabled': None},
        {'first_name': 'John', 'last_name': 'Applebaum', 'email': 'johnnyA@user.com',
         'id': 3, 'team_id': 1, 'disabled': None},
        {'first_name': 'Bill', 'last_name': 'McSorley', 'email': 'billy-max@rocks.com',
         'id': 4, 'team_id': 2, 'disabled': None}]


@pytest.mark.parametrize(
    argnames=['user_id', 'status_code', 'expected_response'],
    argvalues=[
        (1, status.HTTP_200_OK, {
            'first_name': 'Bob', 'last_name': 'Smith',
            'email': 'bob@smith.com', 'id': 1, 'team_id': 1, 'disabled': None}),
        (4, status.HTTP_200_OK, {
            'first_name': 'Bill', 'last_name': 'McSorley',
            'email': 'billy-max@rocks.com', 'id': 4, 'team_id': 2, 'disabled': None}),
        (0, status.HTTP_404_NOT_FOUND, {'detail': 'User not found'}),
        ('bad_user_id', status.HTTP_422_UNPROCESSABLE_ENTITY, {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'}]})])
def test_get_user_responses_with_diff_inputs(
        user_id: int,
        status_code: int,
        expected_response: dict,
        test_app: TestClient,
        test_db_seeded: Session):
    response = test_app.get(f'/users/{user_id}')
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    argnames=['user_id', 'status_code', 'expected_response'],
    argvalues=[
        (1, status.HTTP_200_OK, {'id': 1, 'team_name': 'Marketing'}),
        (4, status.HTTP_200_OK, {'id': 2, 'team_name': 'Engineering'}),
        (0, status.HTTP_404_NOT_FOUND, {'detail': 'User not found'}),
        ('bad_user_id', status.HTTP_422_UNPROCESSABLE_ENTITY, {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'}]})])
def test_get_user_team_responses_with_diff_inputs(
        user_id: int,
        status_code: int,
        expected_response: dict,
        test_app: TestClient,
        test_db_seeded: Session):
    response = test_app.get(f'/users/{user_id}/team')
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    argnames=['user_id', 'field', 'value', 'status_code', 'expected_response'],
    argvalues=[
        (1, 'first_name', 'John', status.HTTP_200_OK, {
            'first_name': 'John', 'last_name': 'Smith', 'email': 'bob@smith.com',
            'id': 1, 'team_id': 1, 'disabled': None}),
        (2, 'email', 'wrong@user.com', status.HTTP_401_UNAUTHORIZED, {
            'detail': 'Could not validate credentials'}),
        (0, 'team_id', 1, status.HTTP_404_NOT_FOUND, {'detail': 'User not found'}),
        ('bad_user_id', 'team_id', 1, status.HTTP_422_UNPROCESSABLE_ENTITY, {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'}]})])
def test_update_user_responses_with_diff_inputs(
        user_id: int,
        field: str,
        value: str,
        status_code: int,
        expected_response: dict,
        test_app: TestClient,
        test_db_seeded: Session):
    payload = json.dumps({'user_schema': {field: value}})
    response = test_app.put(f'/users/{user_id}', data=payload)
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    argnames=['user_id', 'status_code', 'expected_response'],
    argvalues=[
        (1, status.HTTP_200_OK, {
            'first_name': 'Bob', 'last_name': 'Smith',
            'email': 'bob@smith.com', 'id': 1, 'team_id': 1, 'disabled': None}),
        (2, status.HTTP_401_UNAUTHORIZED, {'detail': 'Could not validate credentials'}),
        (0, status.HTTP_404_NOT_FOUND, {'detail': 'User not found'}),
        ('bad_user_id', status.HTTP_422_UNPROCESSABLE_ENTITY, {
            'detail': [{
                'loc': ['path', 'user_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'}]})])
def test_delete_user_responses_with_diff_inputs(
        user_id: int,
        status_code: int,
        expected_response: dict,
        test_app: TestClient,
        test_db_seeded: Session):
    response = test_app.delete(f'/users/{user_id}')
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    argnames=[
        'first_name',
        'last_name',
        'email',
        'password',
        'status_code',
        'expected_response'],
    argvalues=[
        ('Charlotte', 'Kim', 'ck@mail.com', 'test_password', status.HTTP_201_CREATED, {
            'first_name': 'Charlotte', 'last_name': 'Kim',
            'email': 'ck@mail.com', 'id': 5, 'team_id': None, 'disabled': None}),
        ('Existing', 'User', 'billy-max@rocks.com', 'password',
         status.HTTP_400_BAD_REQUEST, {'detail': 'Email already registered'}),
        ('Missing', 'Password', 'm@p.com', None, status.HTTP_422_UNPROCESSABLE_ENTITY, {
            "detail": [{
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing"}]})])
def test_create_user_responses_with_diff_inputs(
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        status_code: int,
        expected_response: dict,
        test_app: TestClient,
        test_db_seeded: Session):
    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password}
    if payload['password'] is None:
        del payload['password']
    response = test_app.post('/users/', data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json() == expected_response
