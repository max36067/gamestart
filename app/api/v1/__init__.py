from . import test, game, user
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(test.router, prefix="/test", tags=["Test"])
router.include_router(game.router, prefix="/games", tags=["Games"])
router.include_router(user.router, prefix="/users", tags=["Users"])
