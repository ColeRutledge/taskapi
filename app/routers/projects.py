from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm.session import Session

from app import crud, schemas, models
from app.db import get_db


router = APIRouter()


@router.get('/', response_model=list[schemas.Project])
def get_all_projects(db: Session = Depends(get_db)):
    return crud.read_all(db, models.Project)


@router.get('/{project_id}', response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project: models.Project = crud.read(db, project_id, models.Project)
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return db_project


@router.get('/{project_id}/data', response_model=schemas.ProjectData)
def get_project_data(project_id: int, db: Session = Depends(get_db)):
    db_project: models.Project = crud.read(db, project_id, models.Project)
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return db_project.get_project_data()


@router.get('/{project_id}/columns', response_model=list[schemas.Column])
def get_project_columns(project_id: int, db: Session = Depends(get_db)):
    db_project: models.Project = crud.read(db, project_id, models.Project)
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return db_project.columns


@router.post('/', response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectBase, db: Session = Depends(get_db)):
    return crud.create(db, project, models.Project)


@router.put('/{project_id}', response_model=schemas.Project)
def update_project(
        project_id: int,
        project: schemas.ProjectUpdate = Body(..., embed=True),
        db: Session = Depends(get_db)):
    db_project: models.Project = crud.read(db, project_id, models.Project)
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return crud.update_project(db, project, db_project)


@router.delete('/{project_id}', response_model=schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project: models.Project = crud.read(db, project_id, models.Project)
    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail='Project not found')
    return crud.delete(db, db_project)
