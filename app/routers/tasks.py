from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm.session import Session

from app import crud, schemas, models
from app.db import get_db


router = APIRouter()


@router.get('/', response_model=list[schemas.Task])
def get_all_tasks(db: Session = Depends(get_db)):
    return crud.read_all(db, models.Task)


@router.get('/{task_id}', response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.read(db, task_id, models.Task)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found')
    return db_task


@router.post('/', response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskBase, db: Session = Depends(get_db)):
    return crud.create(db, task, models.Task)


@router.put('/{task_id}', response_model=schemas.Task)
def update_Task(
        task_id: int,
        task: schemas.TaskUpdate = Body(..., embed=True),
        db: Session = Depends(get_db)):
    db_task = crud.read(db, task_id, models.Task)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found')
    return crud.update(db, task, db_task)


@router.delete('/{task_id}', response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.read(db, task_id, models.Task)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found')
    return crud.delete(db, db_task)
