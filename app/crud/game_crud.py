from sqlalchemy.orm import Session

from app.models import Game

from .crud_base import CRUDBase


class GameCRUD(CRUDBase):
    def get_user_by_name(self, db: Session, game_name: str):
        game = db.query(self.model).filter(self.model.name == game_name).first()
        return game


game = GameCRUD(Game)
