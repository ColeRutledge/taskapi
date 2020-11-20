from fastapi import APIRouter, Depends, HTTPException
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


@router.delete('/{task_id}', response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    crud.delete_task(db, task=db_task)
    return db_task
