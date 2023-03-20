from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import password_hash, verify_password
from app.models import User
from app.schemas import UserCreate

from .crud_base import CRUDBase


class UserCRUD(CRUDBase):
    def get_user_by_email(self, db: Session, email: str):
        user = db.query(self.model).filter(self.model.email == email).first()
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=password_hash(obj_in.password),
            name=obj_in.name,
            is_super_user=obj_in.is_super_user,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authanticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_user_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    def is_active(self, user: User):
        return user.is_active

    def is_super_user(self, user: User):
        return user.is_super_user


user = UserCRUD(User)
