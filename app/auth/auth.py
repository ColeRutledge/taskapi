from app import crud, schemas, models
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from app.db import get_db
from app.main import app_config


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Create a utility function to verify if a received password matches the hash stored.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create a utility function to hash a password coming from the user.
def get_password_hash(password):
    return pwd_context.hash(password)


# And another one to authenticate and return a user.
def authenticate_user(db: Session, email: str, password: str):
    user: models.User = crud.get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# def get_user(db: Session, email: str):
#     if email in db:
#         user_dict = db[email]
#         return schemas.User(**user_dict)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data_to_encode.update({'exp': expire})
    return jwt.encode(data_to_encode, app_config.secret_key, app_config.algorithm)
