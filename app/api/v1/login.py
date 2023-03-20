from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from fastapi.security import OAuth2PasswordRequestForm
from app import crud, models, schemas
from datetime import timedelta
from app.core.config import setting
from app.core import security


router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def user_login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = crud.user.authanticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=setting.access_token_expire_minutes)

    return security.create_access_token(user.email, expire_delta=access_token_expires)


@router.post("/login/test-token")
def test_token(currnet_user: models.User = Depends(deps.get_current_user)) -> Any:
    return currnet_user
