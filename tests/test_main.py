from pathlib import Path

from fastapi.testclient import TestClient

from app.main import startup_event, app


HTTP_200_OK = 200


def test_startup_event():
    log_dir = Path() / 'logs'
    log_file = log_dir / 'debug.log'
    startup_event()
    assert log_dir.exists()
    assert log_dir.is_dir()
    assert log_file.exists()


def test_user_login():
    test_app = TestClient(app)
    response = test_app.get('/')
    assert response.status_code == HTTP_200_OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
