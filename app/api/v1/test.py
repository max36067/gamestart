from fastapi import APIRouter

from app.core.config import setting

router = APIRouter()


@router.get("/")
def get_db_setting():
    uri = setting.database_uri
    return {"db_uri": uri}
