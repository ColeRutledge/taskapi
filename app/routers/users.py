from fastapi import APIRouter, Depends, HTTPException, Body, status
from app.db import get_db
from app import crud, schemas, models
from sqlalchemy.orm.session import Session


router = APIRouter()


@router.get('/', response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.read_all(db=db, model=models.User)


@router.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return db_user


@router.get('/{user_id}/team', response_model=schemas.Team)
def get_user_team(user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return db_user.team


@router.put('/{user_id}', response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return crud.update_user(db, schema=user, model=db_user)


@router.delete('/{user_id}', response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = crud.read(db=db, id=user_id, model=models.User)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    return crud.delete(db=db, resource=db_user)


@router.post('/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
