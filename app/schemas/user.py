from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    user_email: str


class UserCreate(UserBase):
    user_password: str
    is_super_user: bool


class UserUpdate(UserBase):
    user_password: str
    is_active: bool


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
