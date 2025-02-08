import asyncio
import logging
from datetime import datetime
from typing import AsyncGenerator, Dict, Any, Set

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

from data.config import BATCH_SIZE
from data.gifts import GIFT_MAPPINGS
from .core.abstract import BaseParser
from .core.client import ClientManager


class GiftParser(BaseParser):
    def __init__(self):
        self.client_manager = ClientManager()
        self.parsed_users: Set[int] = set()
        self.rate_limit_delay = 0.1
        self.last_request_time = datetime.now()
        self.batch_size = BATCH_SIZE

    async def _handle_rate_limit(self):
        now = datetime.now()
        time_passed = (now - self.last_request_time).total_seconds()
        if time_passed < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_passed)
        self.last_request_time = datetime.now()

    async def get_total_members(self, chat: str) -> int:
        try:
            client = await self.client_manager.get_client()
            if not client:
                return 0
            chat_info = await client.get_chat(chat)
            return chat_info.members_count or 0
        except Exception as e:
            logging.error(f"Error getting total members: {e}")
            return 0

    async def process_member_batch(self, client, members):
        results = []
        processed_count = 0

        for member in members:
            processed_count += 1
            if not member.user or member.user.id in self.parsed_users:
                continue

            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]:
                continue

            self.parsed_users.add(member.user.id)
            try:
                gifts = []
                async for gift in client.get_user_gifts(member.user.id):
                    if (gift.is_limited and
                            gift.is_upgraded is None and
                            str(gift.id) in GIFT_MAPPINGS):
                        gifts.append({
                            "gift": gift.id,
                            "gift_name": GIFT_MAPPINGS[str(gift.id)]["name"],
                            "user_id": member.user.id,
                            "username": member.user.username or "unknown"
                        })

                if gifts:
                    results.append({"gifts": gifts, "processed": processed_count})

            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as e:
                logging.error(f"Error processing user {member.user.id}: {e}")

        return results, processed_count

    async def parse_members(self, chat: str) -> AsyncGenerator[Dict[str, Any], None]:
        client = await self.client_manager.get_client()
        if not client:
            return

        try:
            members_batch = []
            total_processed = 0

            async for member in client.get_chat_members(chat):
                try:
                    members_batch.append(member)

                    if len(members_batch) >= self.batch_size:
                        results, processed = await self.process_member_batch(client, members_batch)
                        total_processed += processed
                        for result in results:
                            result["total_processed"] = total_processed
                            yield result
                        members_batch = []
                        await asyncio.sleep(0.1)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    continue
                except Exception as e:
                    logging.error(f"Error in parse_members batch: {e}")
                    await asyncio.sleep(1)
                    continue

            if members_batch:
                results, processed = await self.process_member_batch(client, members_batch)
                total_processed += processed
                for result in results:
                    result["total_processed"] = total_processed
                    yield result

        except Exception as e:
            logging.error(f"Error in parse_members: {e}")
        finally:
            self.parsed_users.clear()

    async def parse(self, chat: str):
        try:
            async for result in self.parse_members(chat):
                yield result
        except Exception as e:
            logging.error(f"Parse error: {e}")
