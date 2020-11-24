from app import schemas
from app.models import User
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
# from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from app.db import get_db
from app.main import app_config


SECRET_KEY = app_config.secret_key
ALGORITHM = app_config.algorithm

# pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# utility function to verify if a received password matches the hash stored.
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# utility function to hash a password coming from the user.
# def get_password_hash(password):
#     return pwd_context.hash(password)


# utility function to authenticate and return a user. OAuth spec
# requires username vs email while crud is looking up a user via email
# def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
#     user: models.User = crud.get_user_by_email(db=db, email=username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta\
        else datetime.utcnow() + timedelta(minutes=15)
    data_to_encode.update({'exp': expire})
    return jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = \
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail='Could not validate credentials',
                      headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = User.get_user_by_email(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
