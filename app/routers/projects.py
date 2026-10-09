from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm.session import Session

from app import crud, schemas, models
from app.db import get_db
from app.auth.auth_utils import get_current_user
from app.auth.team_access import (
    get_project as get_accessible_project,
    require_team_access,
)


router = APIRouter()


@router.get('/', response_model=list[schemas.Project])
def get_all_projects(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    if current_user.team_id is None:
        return []
    return (
        db.query(models.Project)
        .filter(models.Project.team_id == current_user.team_id)
        .limit(100)
        .all()
    )


@router.get('/{project_id}', response_model=schemas.Project)
def get_project_by_id(
        project_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return get_accessible_project(db, project_id, current_user)


@router.get('/{project_id}/data', response_model=schemas.ProjectData)
def get_project_data(
        project_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_project = get_accessible_project(
        db,
        project_id,
        current_user)
    return db_project.get_project_data()


@router.get('/{project_id}/columns', response_model=list[schemas.Column])
def get_project_columns(
        project_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_project = get_accessible_project(
        db,
        project_id,
        current_user)
    return db_project.columns


@router.post('/', response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
        project: schemas.ProjectBase,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    require_team_access(project.team_id, current_user, 'Team')
    return crud.create(db, project, models.Project)


@router.put('/{project_id}', response_model=schemas.Project)
def update_project(
        project_id: int,
        project: schemas.ProjectUpdate = Body(..., embed=True),
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_project = get_accessible_project(
        db,
        project_id,
        current_user)
    if project.team_id is not None:
        require_team_access(project.team_id, current_user, 'Team')
    return crud.update(db, project, db_project)


@router.delete('/{project_id}', response_model=schemas.Project)
def delete_project(
        project_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_project = get_accessible_project(
        db,
        project_id,
        current_user)
    return crud.delete(db, db_project)
