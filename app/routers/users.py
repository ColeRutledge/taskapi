from fastapi import APIRouter, Depends, HTTPException, Body
from app.db import get_db
from app import crud, schemas
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_users(db=db)


@router.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return db_user


@router.put('/{user_id}', response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return crud.update_user(db, schema=user, model=db_user)


@router.delete('/{user_id}', response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return crud.delete_user(db, user=db_user)


@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
