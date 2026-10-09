from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm.session import Session

from app import models, crud, schemas
from app.db import get_db
from app.auth.auth_utils import get_current_user


router = APIRouter()


@router.get('/', response_model=list[schemas.Team])
def get_all_teams(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.team_id is None:
        return []
    return (
        db.query(models.Team)
        .filter(models.Team.id == current_user.team_id)
        .all()
    )


@router.get('/{team_id}', response_model=schemas.Team)
def get_team(
        team_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if team_id != current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    return db_team


@router.get('/{team_id}/projects', response_model=list[schemas.Project])
def get_team_projects(
        team_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if team_id != current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    return db_team.projects


@router.get('/{team_id}/users', response_model=list[schemas.User])
def get_team_users(
        team_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if team_id != current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    return db_team.users


@router.post('/', response_model=schemas.Team, status_code=status.HTTP_201_CREATED)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    return crud.create(db, team, models.Team)


@router.put('/{team_id}', response_model=schemas.Team)
def update_team(
        team_id: int,
        team: schemas.TeamBase = Body(..., embed=True),
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if team_id != current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    return crud.update(db, team, db_team)


@router.delete('/{team_id}', response_model=schemas.Team)
def delete_team(
        team_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if team_id != current_user.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team not found')
    return crud.delete(db, db_team)
