from fastapi import APIRouter, Depends, HTTPException, Body
from app.db import get_db
from app import crud, schemas, models
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Task])
def get_all_tasks(db: Session = Depends(get_db)):
    return crud.read_all(db=db, model=models.Task)


@router.get('/{task_id}', response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.read(db=db, id=task_id, model=models.Task)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    return db_task


@router.post('/', response_model=schemas.Task)
def create_task(task: schemas.TaskBase, db: Session = Depends(get_db)):
    return crud.create(db=db, body=task, model=models.Task)


@router.put('/{task_id}', response_model=schemas.Task)
def update_Task(
    task_id: int,
    task: schemas.TaskUpdate = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_task = crud.read(db=db, id=task_id, model=models.Task)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    return crud.update_task(db, schema=task, model=db_task)


@router.delete('/{task_id}', response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.read(db=db, id=task_id, model=models.Task)
    if db_task is None:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        )
    return crud.delete(db=db, resource=db_task)
