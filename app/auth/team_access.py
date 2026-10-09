from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from app import crud, models


def require_team_access(
        team_id: int,
        current_user: models.User,
        resource: str) -> None:
    if current_user.team_id != team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{resource} not found')


def get_project(
        db: Session,
        project_id: int,
        current_user: models.User) -> models.Project:
    project = crud.read(db, project_id, models.Project)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project not found')
    require_team_access(project.team_id, current_user, 'Project')
    return project


def get_column(
        db: Session,
        column_id: int,
        current_user: models.User) -> models.Column:
    column = crud.read(db, column_id, models.Column)
    if column is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Column not found')
    get_project(db, column.project_id, current_user)
    return column


def get_task(
        db: Session,
        task_id: int,
        current_user: models.User) -> models.Task:
    task = crud.read(db, task_id, models.Task)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found')
    get_column(db, task.column_id, current_user)
    return task


def accessible_columns(
        db: Session,
        current_user: models.User) -> list[models.Column]:
    if current_user.team_id is None:
        return []
    return (
        db.query(models.Column)
        .join(models.Project)
        .filter(models.Project.team_id == current_user.team_id)
        .limit(100)
        .all()
    )


def accessible_tasks(
        db: Session,
        current_user: models.User) -> list[models.Task]:
    if current_user.team_id is None:
        return []
    return (
        db.query(models.Task)
        .join(models.Column)
        .join(models.Project)
        .filter(models.Project.team_id == current_user.team_id)
        .limit(100)
        .all()
    )
