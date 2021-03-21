from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, crud


def test_get_all_users(monkeypatch, test_app: TestClient):

    def mock_read_all(db: Session, user_model: models.User):
        mock_user = models.User(
            id=1, team_id=1, first_name='Bob',
            last_name='Smith', email='bob@smith.com')
        return [mock_user]

    monkeypatch.setattr(crud, 'read_all', mock_read_all)
    response = test_app.get('/users/')
    assert response.status_code == 200
    assert response.json() == [{
        'first_name': 'Bob', 'last_name': 'Smith', 'id': 1,
        'email': 'bob@smith.com', 'team_id': 1, 'disabled': None}]
