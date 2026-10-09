from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from sqlalchemy.orm.session import Session

from app import models, crud, schemas
from app.db import get_db


router = APIRouter()


@router.get('/', response_model=list[schemas.Team])
def get_all_teams(
        skip: int = Query(
            0,
            ge=0,
            description='Number of teams to skip'),
        limit: int = Query(
            100,
            ge=1,
            le=100,
            description='Maximum number of teams to return'),
        db: Session = Depends(get_db)):
    return crud.read_all(db, models.Team, skip=skip, limit=limit)


@router.get('/{team_id}', response_model=schemas.Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return db_team


@router.get('/{team_id}/projects', response_model=list[schemas.Project])
def get_team_projects(
        team_id: int,
        skip: int = Query(
            0,
            ge=0,
            description='Number of projects to skip'),
        limit: Optional[int] = Query(
            None,
            gt=0,
            le=100,
            description='Maximum number of projects to return'),
        db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return crud.paginate(db_team.projects, skip, limit)


@router.get('/{team_id}/users', response_model=list[schemas.User])
def get_team_users(
        team_id: int,
        skip: int = Query(
            0,
            ge=0,
            description='Number of users to skip'),
        limit: Optional[int] = Query(
            None,
            gt=0,
            le=100,
            description='Maximum number of users to return'),
        db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return crud.paginate(db_team.users, skip, limit)


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
    return crud.update(db, team, db_team)


@router.delete('/{team_id}', response_model=schemas.Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team: models.Team = crud.read(db, team_id, models.Team)
    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail='Team not found')
    return crud.delete(db, db_team)
