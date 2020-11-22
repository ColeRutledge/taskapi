from app import models
from fastapi import APIRouter, Depends, HTTPException, Body
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Team])
def get_all_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db=db)


@router.get('/{team_id}', response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.read(db=db, id=team_id, model=models.Team)
    # db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found',
        )
    return db_team


@router.get('/{team_id}/projects', response_model=list[schemas.Project])
def get_team_projects(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found',
        )
    return db_team.projects


@router.get('/{team_id}/users', response_model=list[schemas.User])
def get_team_users(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found',
        )
    return db_team.users


@router.post('/', response_model=schemas.Team)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    return crud.create(db=db, body=team, schema=schemas.TeamBase, model=models.Team)
    # return crud.create_team(db=db, team=team)


@router.put('/{team_id}', response_model=schemas.Team)
def update_team(
    team_id: int,
    team: schemas.TeamBase = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found',
        )
    return crud.update_team(db, schema=team, model=db_team)


@router.delete('/{team_id}', response_model=schemas.Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found',
        )
    return crud.delete_team(db, team=db_team)
