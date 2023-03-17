from app.db import Base
import sqlalchemy as sa
from sqlalchemy_utils import EmailType, UUIDType
import uuid


class User(Base):
    id = sa.Column(
        UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4
    )
    email = sa.Column(EmailType, index=True, unique=True)
    name = sa.Column(sa.String)
    password = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean(), default=True)
    is_super_user = sa.Column(sa.Boolean(), default=False)
