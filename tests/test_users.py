from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud, schemas


def test_get_all_users(
        test_app: TestClient,
        test_db: Session,
        three_user_schemas: tuple[schemas.UserCreate]):

    for user_schema in three_user_schemas:
        crud.create_user(test_db, user_schema)
    response = test_app.get('/users/')
    response_data = response.json()
    response_data[0]['hashed_password'] = 'mock_hashed_password'
    response_data[1]['hashed_password'] = 'mock_hashed_password'
    response_data[2]['hashed_password'] = 'mock_hashed_password'
    assert response.status_code == 200
    assert response_data == [
        {'first_name': 'test1', 'last_name': 'user1', 'email': 'test1@user.com', 'id': 1,
         'hashed_password': 'mock_hashed_password', 'team_id': None, 'disabled': None},
        {'first_name': 'test2', 'last_name': 'user2', 'email': 'test2@user.com', 'id': 2,
         'hashed_password': 'mock_hashed_password', 'team_id': None, 'disabled': None},
        {'first_name': 'test3', 'last_name': 'user3', 'email': 'test3@user.com', 'id': 3,
         'hashed_password': 'mock_hashed_password', 'team_id': None, 'disabled': None}]
