from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Project])
def get_teams(db: Session = Depends(get_db)):
    return crud.get_projects(db=db)


@router.get('/{project_id}', response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found',
        )
    return db_project


@router.post('/', response_model=schemas.Project)
def create_user(project: schemas.ProjectBase, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)
