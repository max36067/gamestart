from typing import Union
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.db import get_db
from sqlalchemy.orm import Session
from app.schemas import Game, GameCreate
from app import crud, models


router = APIRouter()


@router.get("/", response_model=list[Game])
def get_games(db: Session = Depends(get_db)):
    games = crud.game.get_all()
    return games


@router.get("/{game_id}", response_model=Game)
def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


@router.post("/", response_model=Game)
async def create_game(game: GameCreate, db: Session = Depends(get_db)):
    db_game = models.Game(name=game.name)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


@router.delete("/{game_id}", response_model=dict[str, Union[bool, Game]])
def delete_game_by_id(game_id: int, db: Session = Depends(get_db)):
    db_game = db.get(models.Game, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(db_game)
    db.commit()
    return {"ok": True, "game": db_game}
