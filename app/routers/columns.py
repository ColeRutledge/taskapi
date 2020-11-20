from fastapi import APIRouter, Depends
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.Column])
def get_columns(db: Session = Depends(get_db)):
    return crud.get_columns(db=db)


@router.post('/', response_model=schemas.Column)
def create_column(column: schemas.ColumnBase, db: Session = Depends(get_db)):
    return crud.create_column(db=db, column=column)
