from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm.session import Session

from app import crud, schemas, models
from app.db import get_db
from app.auth.auth_utils import get_current_user
from app.auth.team_access import accessible_tasks, get_column, get_task


router = APIRouter()


@router.get('/', response_model=list[schemas.Task])
def get_all_tasks(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return accessible_tasks(db, current_user)


@router.get('/{task_id}', response_model=schemas.Task)
def get_task_by_id(
        task_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    return get_task(db, task_id, current_user)


@router.post('/', response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
        task: schemas.TaskBase,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    get_column(db, task.column_id, current_user)
    return crud.create(db, task, models.Task)


@router.put('/{task_id}', response_model=schemas.Task)
def update_Task(
        task_id: int,
        task: schemas.TaskUpdate = Body(..., embed=True),
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_task = get_task(db, task_id, current_user)
    if task.column_id is not None:
        get_column(db, task.column_id, current_user)
    return crud.update(db, task, db_task)


@router.delete('/{task_id}', response_model=schemas.Task)
def delete_task(
        task_id: int,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    db_task = get_task(db, task_id, current_user)
    return crud.delete(db, db_task)
