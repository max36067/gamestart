from datetime import datetime, timedelta, timezone
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from redis import Redis

from app.core.config import setting

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
black_list = dict()


def create_access_token(subject: Union[str, Any], expire_delta: timedelta = None):
    iat = datetime.now(tz=timezone.utc)
    if expire_delta:
        expire = iat + expire_delta
    else:
        expire = iat + timedelta(minutes=setting.access_token_expire_minutes)
    to_encode = {"exp": expire, "sub": str(subject), "iat": int(iat.timestamp())}
    encode_jwt = jwt.encode(to_encode, setting.secret_key, algorithm=setting.algorithm)
    return {
        "access_token": encode_jwt,
        "token_type": "Bearer",
        "exp": expire,
    }


def verify_otp():
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def password_hash(password: str):
    return pwd_context.hash(password)


def add_black_list(cache: Redis, token: str):
    payload = jwt.decode(token, setting.secret_key, setting.algorithm)
    cache.set(token, payload.get("exp"))
