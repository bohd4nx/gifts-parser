import asyncio
import logging
from typing import AsyncGenerator, Dict, Any, List

from pyrogram import Client
from pyrogram.enums import ChatMembersFilter

from .get_gifts import get_user_gifts

logger = logging.getLogger(__name__)

BATCH_SIZE = 500
YIELD_INTERVAL = 500


async def get_regular_members(client: Client, chat: str, gift_mappings: Dict) -> AsyncGenerator[Dict[str, Any], None]:
    total_processed = 0
    batch_gifts = []
    last_yield_count = 0
    current_batch = []

    try:
        async for member in client.get_chat_members(chat, filter=ChatMembersFilter.SEARCH):
            if not member.user or member.user.is_bot:
                continue

            current_batch.append(member)

            if len(current_batch) >= BATCH_SIZE:
                processed_gifts = await process_batch(client, current_batch, gift_mappings)
                total_processed += len(current_batch)
                batch_gifts.extend(processed_gifts)
                current_batch = []

                if total_processed - last_yield_count >= YIELD_INTERVAL:
                    logger.info(f"Progress: {total_processed} users processed, {len(batch_gifts)} gifts found")
                    yield {"gifts": batch_gifts, "total_processed": total_processed}
                    batch_gifts = []
                    last_yield_count = total_processed

        if current_batch:
            processed_gifts = await process_batch(client, current_batch, gift_mappings)
            total_processed += len(current_batch)
            batch_gifts.extend(processed_gifts)

        if batch_gifts or total_processed != last_yield_count:
            yield {"gifts": batch_gifts, "total_processed": total_processed}

    except Exception as e:
        logger.error(f"Error parsing {chat}: {e}")


async def process_batch(client: Client, members: List, gift_mappings: Dict) -> List:
    tasks = [
        get_user_gifts(client, m.user.id, m.user.username, gift_mappings)
        for m in members
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    gifts = []
    for result in results:
        if isinstance(result, list) and result:
            gifts.extend(result)

    return gifts
