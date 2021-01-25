from datetime import timedelta

from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm as OAuthForm
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from app.config import get_settings
from app import schemas
from app.auth.auth_utils import create_access_token, get_current_user
from app.db import get_db
from app.models import User


TOKEN_EXPIRES = get_settings().access_token_expires_minutes
router = APIRouter()


@router.post('/token', response_model=schemas.Token)
async def login(form_data: OAuthForm = Depends(), db: Session = Depends(get_db)):
    user = User.authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRES)
    access_token = create_access_token(
        data={'sub': user.email},   # 'sub' is a jwt specification
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/self/me', response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user
