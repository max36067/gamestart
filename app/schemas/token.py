from typing import Union
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expired_time: float


class TokenPayload(BaseModel):
    sub: Union[str, None] = None
