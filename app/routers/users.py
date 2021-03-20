import logging

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm.session import Session

from app import crud, schemas, models
from app.auth.auth_utils import get_current_user as gcu
from app.db import get_db


router = APIRouter()


@router.get('/', response_model=list[schemas.User], dependencies=[Depends(gcu)])
def get_all_users(db: Session = Depends(get_db)):
    return crud.read_all(db=db, model=models.User)


@router.get('/{user_id}', response_model=schemas.User, dependencies=[Depends(gcu)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    return db_user


@router.get('/{user_id}/team', response_model=schemas.Team, dependencies=[Depends(gcu)])
def get_user_team(user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user.team


@router.put('/{user_id}', response_model=schemas.User)
def update_user(
        user_id: int,
        user: schemas.UserUpdate = Body(..., embed=True),
        current_user: models.User = Depends(gcu),
        db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    elif current_user != db_user:
        logging.warning(
            f'User[{current_user.email}] tried to access User[{db_user.email}]')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'})
    return crud.update_user(db, schema=user, model=db_user)


@router.delete('/{user_id}', response_model=schemas.User, dependencies=[Depends(gcu)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found')
    return crud.delete(db=db, resource=db_user)


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered")
    return crud.create_user(db=db, user=user)
