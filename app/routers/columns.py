from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from sqlalchemy.orm.session import Session

from app.db import get_db
from app import crud, schemas, models


router = APIRouter()


@router.get('/', response_model=list[schemas.Column])
def get_all_columns(
        skip: int = Query(
            0,
            ge=0,
            description='Number of columns to skip'),
        limit: int = Query(
            100,
            ge=1,
            le=100,
            description='Maximum number of columns to return'),
        db: Session = Depends(get_db)):
    return crud.read_all(db, models.Column, skip=skip, limit=limit)


@router.get('/{column_id}', response_model=schemas.Column)
def get_column(column_id: int, db: Session = Depends(get_db)):
    db_column: models.Column = crud.read(db, column_id, models.Column)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found')
    return db_column


@router.get('/{column_id}/tasks', response_model=list[schemas.Task])
def get_column_tasks(
        column_id: int,
        skip: int = Query(
            0,
            ge=0,
            description='Number of tasks to skip'),
        limit: Optional[int] = Query(
            None,
            gt=0,
            le=100,
            description='Maximum number of tasks to return'),
        db: Session = Depends(get_db)):
    db_column: models.Column = crud.read(db, column_id, models.Column)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found')
    return crud.paginate(db_column.tasks, skip, limit)


@router.post('/', response_model=schemas.Column, status_code=status.HTTP_201_CREATED)
def create_column(column: schemas.ColumnBase, db: Session = Depends(get_db)):
    return crud.create(db, column, models.Column)


@router.put('/{column_id}', response_model=schemas.Column)
def update_column(
        column_id: int,
        column: schemas.ColumnUpdate = Body(..., embed=True),
        db: Session = Depends(get_db)):
    db_column: models.Column = crud.read(db, column_id, models.Column)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found')
    return crud.update(db, column, db_column)


@router.delete('/{column_id}', response_model=schemas.Column)
def delete_column(column_id: int, db: Session = Depends(get_db)):
    db_column: models.Column = crud.read(db, column_id, models.Column)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found')
    return crud.delete(db, db_column)
