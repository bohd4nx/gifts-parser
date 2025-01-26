import asyncio
import logging
from typing import AsyncGenerator, Dict, Any

from pyrogram.enums import ChatMemberStatus

from .core.abstract import BaseParser
from .core.client import ClientManager


class GiftParser(BaseParser):
    def __init__(self):
        self.client_manager = ClientManager()
        self.max_retries = 3
        self.retry_delay = 1

    async def get_total_members(self, chat: str) -> int:
        try:
            client = await self.client_manager.get_client()
            if not client:
                return 0
            chat_info = await client.get_chat(chat)
            return chat_info.members_count
        except Exception as e:
            logging.error(f"Error getting total members: {e}")
            return 0

    async def parse_members(self, chat: str) -> AsyncGenerator[Dict[str, Any], None]:
        client = None
        for _ in range(self.max_retries):
            try:
                client = await self.client_manager.get_client()
                if not client:
                    continue

                async for user in client.get_chat_members(chat):
                    if user.status == ChatMemberStatus.MEMBER:
                        gifts = await self._get_user_gifts(client, user.user.id, user.user.username)
                        yield gifts
                        await asyncio.sleep(0.5)
                break

            except Exception as e:
                logging.error(f"Error in parse_members: {e}")
                await asyncio.sleep(self.retry_delay)
            finally:
                if client:
                    await self.client_manager.cleanup()

    @staticmethod
    async def _get_user_gifts(client, user_id: int, username: str):
        result = []
        try:
            async for gift in client.get_user_gifts(user_id):
                if gift.is_limited and not gift.is_upgraded:
                    result.append({
                        "gift": gift.id,
                        "user_id": user_id,
                        "username": username
                    })
        except Exception as e:
            logging.error(f"Error getting user gifts: {e}")
            return []

        return result

    async def parse(self, chat: str):
        async for result in self.parse_members(chat):
            yield result
