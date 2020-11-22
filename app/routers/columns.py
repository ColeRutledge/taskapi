from fastapi import APIRouter, Depends, HTTPException, Body
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Column])
def get_all_columns(db: Session = Depends(get_db)):
    return crud.get_columns(db=db)


@router.get('/{column_id}', response_model=schemas.Column)
def get_column(column_id: int, db: Session = Depends(get_db)):
    db_column = crud.get_column(db, column_id=column_id)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found',
        )
    return db_column


@router.get('/{column_id}/tasks', response_model=list[schemas.Task])
def get_column_tasks(column_id: int, db: Session = Depends(get_db)):
    db_column = crud.get_column(db, column_id=column_id)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found',
        )
    return db_column.tasks


@router.post('/', response_model=schemas.Column)
def create_column(column: schemas.ColumnBase, db: Session = Depends(get_db)):
    return crud.create_column(db=db, column=column)


@router.put('/{column_id}', response_model=schemas.Column)
def update_column(
    column_id: int,
    column: schemas.ColumnUpdate = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_column = crud.get_column(db, column_id=column_id)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found',
        )
    return crud.update_column(db, schema=column, model=db_column)


@router.delete('/{column_id}', response_model=schemas.Column)
def delete_column(column_id: int, db: Session = Depends(get_db)):
    db_column = crud.get_column(db, column_id=column_id)
    if db_column is None:
        raise HTTPException(
            status_code=404,
            detail='Column not found',
        )
    return crud.delete_column(db, column=db_column)
