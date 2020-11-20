from fastapi import APIRouter, Depends
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db=db)


@router.post('/', response_model=schemas.Team)
def create_user(team: schemas.TeamBase, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)
