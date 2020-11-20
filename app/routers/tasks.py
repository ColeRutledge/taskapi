from fastapi import APIRouter, Depends, HTTPException, Body
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db=db)


@router.get('/{task_id}', response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    return db_task


@router.post('/', response_model=schemas.Task)
def create_task(task: schemas.TaskBase, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


@router.put('/{task_id}', response_model=schemas.Task)
def update_Task(
    task_id: int,
    task: schemas.TaskBase = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    return crud.update_task(db, schema=task, model=db_task)


@router.delete('/{task_id}', response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    return crud.delete_task(db, task=db_task)
