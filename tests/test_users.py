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


def test_get_user_not_found(test_app: TestClient, test_db_seeded: Session):
    invalid_id = 0
    response = test_app.get(f'/users/{invalid_id}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


@pytest.mark.parametrize(argnames='user_id', argvalues=[1, 2, 3, 4])
def test_get_user_team(user_id: int, test_app: TestClient, test_db_seeded: Session):
    response = test_app.get(f'/users/{user_id}/team')
    assert response.status_code == 200
    assert response.json() in [
        {'id': 1, 'team_name': 'Marketing'},
        {'id': 2, 'team_name': 'Engineering'}]


def test_get_user_team_not_found(test_app: TestClient, test_db_seeded: Session):
    invalid_id = 0
    response = test_app.get(f'/users/{invalid_id}/team')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'
