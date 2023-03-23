from typing import Iterator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import redis

from app import crud, models, schemas
from app.core.config import setting
from app.db.session import SessionLocal
from app.db.redis import pool

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session"""
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


def get_redis():
    return redis.Redis(connection_pool=pool)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get_by_email(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def verify_jwt_token(
    cache: redis.Redis = Depends(get_redis), token: str = Depends(reusable_oauth2)
):
    if cache.get(token):
        raise HTTPException(status_code=400, detail="JWT token invalid")
