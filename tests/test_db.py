import os
from collections import namedtuple

import pytest
from sqlalchemy.orm import Session

from app import db, models, crud, schemas
from app.models import Base
from tests.conftest import TestSessionLocal, engine


def test_get_db(monkeypatch):
    monkeypatch.setattr(db, 'SessionLocal', TestSessionLocal)
    Base.metadata.create_all(bind=engine, checkfirst=True)

    session: Session = next(db.get_db())
    team_schema = schemas.TeamBase(team_name='QA')
    team_from_create = crud.create(session, team_schema, models.Team)
    team_from_read = crud.read(session, 1, models.Team)
    assert isinstance(team_from_create, models.Team)
    assert isinstance(team_from_read, models.Team)
    assert team_from_create.team_name == team_from_read.team_name

    Base.metadata.drop_all(bind=engine)


@pytest.mark.parametrize(
    argnames=['environment', 'expected_url'],
    argvalues=[
        ('local', 'sqlite:///app.db'),
        ('container', 'sqlite:///app_test.db')])
def test_create_database_engine(environment: str, expected_url: str, monkeypatch):
    if os.getenv('FASTAPI_ENV'):  # if executing inside container (github actions)
        del os.environ['FASTAPI_ENV']

    SettingsWithURL = namedtuple('SettingsWithUrl', ['db_url'])
    mock_settings = SettingsWithURL(db_url='sqlite:///app_test.db')

    def mock_get_settings():
        return mock_settings

    monkeypatch.setattr(db, 'get_settings', mock_get_settings)

    if environment == 'container':
        os.environ['FASTAPI_ENV'] = 'development'
        engine = db.create_database_engine()
    else:
        engine = db.create_database_engine()

    assert str(engine.url) == expected_url
