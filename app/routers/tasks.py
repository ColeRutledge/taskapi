from fastapi import APIRouter, Depends
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Task])
def get_teams(db: Session = Depends(get_db)):
    return crud.get_tasks(db=db)


@router.post('/', response_model=schemas.Task)
def create_user(task: schemas.TaskBase, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)
