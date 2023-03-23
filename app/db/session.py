from typing import Iterator

import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import setting

engine = sa.engine.create_engine(setting.database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
