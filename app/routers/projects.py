from fastapi import APIRouter, Depends
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Project])
def get_teams(db: Session = Depends(get_db)):
    return crud.get_projects(db=db)


@router.post('/', response_model=schemas.Project)
def create_user(project: schemas.ProjectBase, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)
