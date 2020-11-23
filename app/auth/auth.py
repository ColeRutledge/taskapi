from app.crud import get_user_by_email
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


SECRET_KEY = app_config.secret_key
ALGORITHM = app_config.algorithm

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


# Create a utility function to verify if a received password matches the hash stored.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create a utility function to hash a password coming from the user.
def get_password_hash(password):
    return pwd_context.hash(password)


# And another one to authenticate and return a user.
def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    user: models.User = crud.get_user_by_email(db=db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data_to_encode.update({'exp': expire})
    return jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = \
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                      detail='Could not validate credentials',
                      headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
