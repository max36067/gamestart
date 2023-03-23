from sqlalchemy.orm import Session

from app.models import Salt

from .crud_base import CRUDBase


class SaltCRUD(CRUDBase):
    def get_by_email(self, db: Session, email: str):
        return db.query(self.model).filter(self.model.email == email).first()


salt = SaltCRUD(Salt)
