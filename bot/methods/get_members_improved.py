import asyncio
import logging
from string import ascii_lowercase
from typing import AsyncGenerator, Dict, Any, Set

from pyrogram import Client
from pyrogram import raw
from pyrogram.errors import FloodWait

from .get_gifts import get_user_gifts

logger = logging.getLogger(__name__)

BATCH_SIZE = 300
YIELD_INTERVAL = 300
QUERY_LIMIT = 200
MAX_OFFSET = 10000


async def get_large_members(client: Client, chat: str, gift_mappings: Dict) -> AsyncGenerator[Dict[str, Any], None]:
    processed_users: Set[int] = set()
    total_processed = 0
    queries = [""] + [str(i) for i in range(10)] + list(ascii_lowercase)
    batch_gifts = []
    last_yield_count = 0

    try:
        peer = await client.resolve_peer(chat)

        for query in queries:
            offset = 0

            while offset <= MAX_OFFSET:
                try:
                    participants = await client.invoke(
                        raw.functions.channels.GetParticipants(
                            channel=peer,
                            filter=raw.types.ChannelParticipantsSearch(q=query),
                            offset=offset,
                            limit=QUERY_LIMIT,
                            hash=0
                        )
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    continue

                if not participants.participants:
                    break

                new_users = [
                    user for user in participants.users
                    if not user.bot and user.id not in processed_users
                ]

                for i in range(0, len(new_users), BATCH_SIZE):
                    user_batch = new_users[i:i + BATCH_SIZE]
                    tasks = []

                    for user in user_batch:
                        processed_users.add(user.id)
                        total_processed += 1
                        tasks.append(get_user_gifts(client, user.id, user.username, gift_mappings))

                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    batch_gifts.extend([gift for result in results
                                        if isinstance(result, list) and result
                                        for gift in result])

                    if total_processed - last_yield_count >= YIELD_INTERVAL:
                        logger.info(f"Progress: {total_processed} users processed, {len(batch_gifts)} gifts found")
                        yield {"gifts": batch_gifts, "total_processed": total_processed}
                        batch_gifts = []
                        last_yield_count = total_processed

                offset += len(participants.participants)

        if batch_gifts or total_processed != last_yield_count:
            yield {"gifts": batch_gifts, "total_processed": total_processed}

        logger.info(f"Completed parsing {chat}: {total_processed} users processed")

    except Exception as e:
        logger.error(f"Error parsing {chat}: {e}")
