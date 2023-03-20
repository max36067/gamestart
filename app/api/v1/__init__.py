from . import test, game, user, login
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(test.router, prefix="/test", tags=["Test"])
router.include_router(game.router, prefix="/games", tags=["Games"])
router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(login.router, tags=["Login"])
