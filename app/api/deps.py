from typing import Iterator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


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


def get_current_user():
    pass
