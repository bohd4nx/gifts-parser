from aiogram import Router

from .core.client import ClientManager
from .handlers.parse import router as parse_router
from .handlers.start import router as start_router
from .settings import GiftParser
from .utils.helper import BotCommands

router = Router()
router.include_router(start_router)
router.include_router(parse_router)

client_manager = ClientManager()
gift_parser = GiftParser()


async def get_client():
    return await client_manager.get_client()


async def parse_members(chat):
    return gift_parser.parse_members(chat)


async def get_chat_gifts(chat_id, **kwargs):
    client = await get_client()
    if client:
        return client.get_chat_gifts(chat_id, **kwargs)
    return []


__all__ = [
    "get_client",
    "get_chat_gifts",
    "parse_members",
    "router",
    "BotCommands"
]
