from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: Union[str, Any], expire_delta: timedelta = None):
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=setting.access_token_expire_minutes
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, setting.secret_key, algorithm=setting.algorithm)
    return {
        "access_token": encode_jwt,
        "token_type": "Bearer",
        "expired_time": int(expire.timestamp()),
    }


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password: str):
    return pwd_context.hash(password)
