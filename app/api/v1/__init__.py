from fastapi import APIRouter, Depends
from . import game, login, test, user
from app.api import deps

router = APIRouter(prefix="/api/v1")

router.include_router(test.router, prefix="/test", tags=["Test"])
router.include_router(
    game.router,
    prefix="/games",
    dependencies=[Depends(deps.verify_jwt_token)],
    tags=["Games"],
)
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(login.router, tags=["Login"])
