from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from fastapi.exceptions import HTTPException

router = APIRouter()

# TODO: Need jwt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/")
def create_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    user = crud.user.get_user_by_email(db=db, email=user_in.user_email)
    if user:
        raise HTTPException(status_code=400, detail="User is already exists.")

    # Need a certificate with superuser
    user = crud.user.create(db=db, obj_in=user_in)

    return user


@router.get("/")
def get_me(db: Session = Depends(deps.get_db), token: str = Depends(oauth2_scheme)):
    return {"token": token}
