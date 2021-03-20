import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_all_users(test_app: TestClient, test_db_seeded: Session):
    response = test_app.get('/users/')
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == [
        {'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob@smith.com',
         'id': 1, 'team_id': 1, 'disabled': None},
        {'first_name': 'Sally', 'last_name': 'McBeth', 'email': 'Sally@123.com',
         'id': 2, 'team_id': 1, 'disabled': None},
        {'first_name': 'John', 'last_name': 'Applebaum', 'email': 'johnnyA@user.com',
         'id': 3, 'team_id': 1, 'disabled': None},
        {'first_name': 'Bill', 'last_name': 'McSorley', 'email': 'billy-max@rocks.com',
         'id': 4, 'team_id': 2, 'disabled': None}]


@pytest.mark.parametrize(argnames='user_id', argvalues=[1, 2, 3, 4])
def test_get_user(user_id: int, test_app: TestClient, test_db_seeded: Session):
    response = test_app.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json() in [
        {'first_name': 'Bob', 'last_name': 'Smith', 'email': 'bob@smith.com',
         'id': 1, 'team_id': 1, 'disabled': None},
        {'first_name': 'Sally', 'last_name': 'McBeth', 'email': 'Sally@123.com',
         'id': 2, 'team_id': 1, 'disabled': None},
        {'first_name': 'John', 'last_name': 'Applebaum', 'email': 'johnnyA@user.com',
         'id': 3, 'team_id': 1, 'disabled': None},
        {'first_name': 'Bill', 'last_name': 'McSorley', 'email': 'billy-max@rocks.com',
         'id': 4, 'team_id': 2, 'disabled': None}]


def test_get_user_invalid(test_app: TestClient, test_db_seeded: Session):
    invalid_user_id = 0
    response = test_app.get(f'/users/{invalid_user_id}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


@pytest.mark.parametrize(argnames='user_id', argvalues=[1, 2, 3, 4])
def test_get_user_team(user_id: int, test_app: TestClient, test_db_seeded: Session):
    response = test_app.get(f'/users/{user_id}/team')
    assert response.status_code == 200
    assert response.json() in [
        {'id': 1, 'team_name': 'Marketing'},
        {'id': 2, 'team_name': 'Engineering'}]


def test_get_user_team_invalid(test_app: TestClient, test_db_seeded: Session):
    invalid_user_id = 0
    response = test_app.get(f'/users/{invalid_user_id}/team')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


def test_update_user(test_app: TestClient, test_db_seeded: Session):
    user_id = 1
    put_response = test_app.put(
        f'/users/{user_id}',
        data=json.dumps({
            'user': {
                'first_name': 'John',       # updating from 'Bob'
                'last_name': 'Smith',
                'email': 'john@smith.com',  # updating from 'bob@smith.com'
                'password': 'password',
                'team_id': 1,
                'disabled': False}}))
    get_response = test_app.get(f'/users/{user_id}')
    assert put_response.status_code == 200
    assert put_response.json() == get_response.json()
