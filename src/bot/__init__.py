from aiogram import Router

from .handlers.parse import router as parse_router
from .handlers.start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(parse_router)

__all__ = [
    "get_client",
    "get_user_gifts",
    "parse_members",
    "router"
]
