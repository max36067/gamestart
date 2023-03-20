import sqlalchemy as sa
from sqlalchemy_utils import EmailType

from app.db import Base


class User(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    email = sa.Column(EmailType, index=True, unique=True)
    name = sa.Column(sa.String)
    password = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean(), default=True)
    is_super_user = sa.Column(sa.Boolean(), default=False)
