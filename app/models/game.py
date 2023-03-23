import sqlalchemy as sa

from app.db import Base


class Game(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, nullable=False)
