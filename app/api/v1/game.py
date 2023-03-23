from typing import Union

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.schemas import Game, GameCreate

router = APIRouter()


@router.get("/", response_model=list[Game])
def get_games(db: Session = Depends(deps.get_db)):
    games = crud.game.get_all(db=db)
    return games


@router.get("/{game_id}", response_model=Game)
def get_game_by_id(game_id: int, db: Session = Depends(deps.get_db)):
    game = crud.game.get(db=db, id=game_id)
    return game


@router.post("/", response_model=Game)
async def create_game(game_in: GameCreate, db: Session = Depends(deps.get_db)):
    game = crud.game.get_user_by_name(db, game_in.name)
    if game:
        raise HTTPException(
            status_code=400, detail="The Game with this name already exists in system."
        )
    game = crud.game.create(db, obj_in=game_in)
    return game


@router.delete("/{game_id}", response_model=dict[str, Union[bool, Game]])
def delete_game_by_id(game_id: int, db: Session = Depends(deps.get_db)):
    db_game = crud.game.get(db=db, id=game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    game = crud.game.remove(db=db, id=game_id)
    return game
