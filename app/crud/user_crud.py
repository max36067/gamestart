from secrets import token_hex
from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import password_hash, verify_password
from app.models import Salt, User
from app.schemas import UserCreate

from .crud_base import CRUDBase
from .salt_crud import salt


class UserCRUD(CRUDBase):
    def get_by_email(self, db: Session, email: str):
        user = db.query(self.model).filter(self.model.email == email).first()
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        salt = token_hex(16)
        salted_password = obj_in.password + salt

        db_obj = User(
            email=obj_in.email,
            password=password_hash(salted_password),
            name=obj_in.name,
            is_super_user=obj_in.is_super_user,
        )
        salt_obj = Salt(email=obj_in.email, salt=salt)
        db.add_all([db_obj, salt_obj])
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authanticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db=db, email=email)
        if not user:
            return None
        salt_token = salt.get_by_email(db=db, email=email)
        salted_password = password + salt_token.salt
        if not verify_password(salted_password, user.password):
            return None
        return user

    def is_active(self, user: User):
        return user.is_active

    def is_super_user(self, user: User):
        return user.is_super_user


user = UserCRUD(User)
