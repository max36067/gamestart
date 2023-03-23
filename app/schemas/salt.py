from pydantic import BaseModel


class SaltBase(BaseModel):
    email: str
    salt: str


class SaltCreate(SaltBase):
    pass


class Salt(SaltBase):
    class Config:
        orm_mode = True
