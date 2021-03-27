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
