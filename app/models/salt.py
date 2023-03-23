import sqlalchemy as sa
from sqlalchemy_utils import EmailType

from app.db import Base


class Salt(Base):
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(EmailType, index=True, unique=True)
    salt = sa.Column(sa.String)
