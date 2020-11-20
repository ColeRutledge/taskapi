from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Team])
def get_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db=db)


@router.get('/{team_id}', response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found',
        )
    return db_team


@router.post('/', response_model=schemas.Team)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    return crud.create_team(db=db, team=team)


@router.delete('/{team_id}', response_model=schemas.Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found',
        )
    crud.delete_team(db, team=db_team)
    return db_team
