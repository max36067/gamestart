from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from redis import Redis
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import setting

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def user_login(
    response: Response,
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
    token = security.create_access_token(user.email, expire_delta=access_token_expires)
    cookie_expires = token.pop("exp")
    response.set_cookie(
        key="t",
        value=token,
        expires=cookie_expires,
        httponly=True,
    )
    return token


@router.post("/logout")
def user_logout(
    cache: Redis = Depends(deps.get_redis), token: str = Depends(deps.reusable_oauth2)
):
    security.add_black_list(cache, token)
    resp = RedirectResponse("/", status_code=302)
    resp.delete_cookie("t")
    return resp


@router.post("/login/test-token")
def test_token(currnet_user: models.User = Depends(deps.get_current_user)) -> Any:
    return currnet_user
