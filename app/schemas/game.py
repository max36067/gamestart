from pydantic import BaseModel


class GameBase(BaseModel):
    name: str


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class Game(GameBase):
    id: int
    name: str

    class Config:
        orm_mode = True
