from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import setting

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    user = crud.user.get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="User is already exists.")

    # Need current super user to create user
    user = crud.user.create(db=db, obj_in=user_in)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user)


@router.get("/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user
