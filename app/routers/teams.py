from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm.session import Session

from app import models, crud, schemas
from app.db import get_db


router = APIRouter()


@router.get('/', response_model=list[schemas.Team])
def get_all_teams(db: Session = Depends(get_db)):
    return crud.read_all(db, models.Team)


@router.get('/{team_id}', response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return db_team


@router.get('/{team_id}/projects', response_model=list[schemas.Project])
def get_team_projects(team_id: int, db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return db_team.projects


@router.get('/{team_id}/users', response_model=list[schemas.User])
def get_team_users(team_id: int, db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return db_team.users


@router.post('/', response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    return crud.create(db, team, models.Team)


@router.put('/{team_id}', response_model=schemas.Team)
def update_team(
        team_id: int,
        team: schemas.TeamBase = Body(..., embed=True),
        db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return crud.update_team(db, team, db_team)


@router.delete('/{team_id}', response_model=schemas.Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return crud.delete(db, db_team)
