from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_all_users(test_app: TestClient, test_db_with_three_users: Session):
    response = test_app.get('/users/')
    response_data = response.json()
    response_data[0]['hashed_password'] = 'mock_hashed_password'
    response_data[1]['hashed_password'] = 'mock_hashed_password'
    response_data[2]['hashed_password'] = 'mock_hashed_password'
    response_data[3]['hashed_password'] = 'mock_hashed_password'
    assert response.status_code == 200
    assert response_data == [
        {'first_name': 'test1', 'last_name': 'user1', 'email': 'test1@user.com', 'id': 1,
         'hashed_password': 'mock_hashed_password', 'team_id': 1, 'disabled': None},
        {'first_name': 'test2', 'last_name': 'user2', 'email': 'test2@user.com', 'id': 2,
         'hashed_password': 'mock_hashed_password', 'team_id': 1, 'disabled': None},
        {'first_name': 'test3', 'last_name': 'user3', 'email': 'test3@user.com', 'id': 3,
         'hashed_password': 'mock_hashed_password', 'team_id': 1, 'disabled': None},
        {'first_name': 'test4', 'last_name': 'user4', 'email': 'test4@user.com', 'id': 4,
         'hashed_password': 'mock_hashed_password', 'team_id': 2, 'disabled': None}]
