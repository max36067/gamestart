from .crud_base import CRUDBase
from app.models import Game


class GameCRUD(CRUDBase):
    pass


game = GameCRUD(Game)
