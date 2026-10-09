from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm.session import Session

from app.db import get_db
from app import crud, schemas, models
from app.auth.auth_utils import get_current_user
from app.auth.team_access import (
    accessible_columns,
    get_column,
    get_project,
)


router = APIRouter()


@router.get('/', response_model=list[schemas.Column])
def get_all_columns(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return accessible_columns(db, current_user)


@router.get('/{column_id}', response_model=schemas.Column)
def get_column_by_id(
        column_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return get_column(db, column_id, current_user)


@router.get('/{column_id}/tasks', response_model=list[schemas.Task])
def get_column_tasks(
        column_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_column = get_column(db, column_id, current_user)
    return db_column.tasks


@router.post('/', response_model=schemas.Column, status_code=status.HTTP_201_CREATED)
def create_column(
        column: schemas.ColumnBase,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    get_project(db, column.project_id, current_user)
    return crud.create(db, column, models.Column)


@router.put('/{column_id}', response_model=schemas.Column)
def update_column(
        column_id: int,
        column: schemas.ColumnUpdate = Body(..., embed=True),
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_column = get_column(db, column_id, current_user)
    if column.project_id is not None:
        get_project(db, column.project_id, current_user)
    return crud.update(db, column, db_column)


@router.delete('/{column_id}', response_model=schemas.Column)
def delete_column(
        column_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_column = get_column(db, column_id, current_user)
    return crud.delete(db, db_column)
