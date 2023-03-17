from typing import Iterator
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import setting

engine = sa.engine.create_engine(setting.database_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterator[Session]:
    """FastAPI dependency that provides a sqlalchemy session"""
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
