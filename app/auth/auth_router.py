from datetime import timedelta
from fastapi.exceptions import HTTPException
from app.auth.auth_utils import authenticate_user, create_access_token
from fastapi import APIRouter, Depends, status
from app import schemas
from app.db import get_db
from sqlalchemy.orm.session import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.main import app_config


TOKEN_EXPIRES = app_config.access_token_expires
router = APIRouter()


@router.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRES)
    access_token = create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires,
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
