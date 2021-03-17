from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import crud


def test_get_all_users(test_app: TestClient, test_db: Session, single_user_schema):
    crud.create_user(test_db, single_user_schema)
    response = test_app.get('/users/')
    mocked_response = response.json()
    mocked_response[0]['hashed_password'] = 'mock_hashed_password'
    assert response.status_code == 200
    assert mocked_response == [{
        'first_name': 'test1',
        'last_name': 'user1',
        'email': 'test1@user.com',
        'id': 1,
        'hashed_password': 'mock_hashed_password',
        'team_id': None,
        'disabled': None}]
