from .crud_base import CRUDBase
from app.models import User
from sqlalchemy.orm import Session


class UserCRUD(CRUDBase):
    def get_user_by_email(self, db: Session, email: str):
        user = db.query(self.model).filter(self.model.email == email).first()
        return user


user = UserCRUD(User)
