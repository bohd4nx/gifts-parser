import asyncio
import logging
from string import ascii_lowercase
from typing import AsyncGenerator, Dict, Any, Set, List

from pyrogram import Client, types
from pyrogram import raw
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from bot.services.gifts import gifts_list

logger = logging.getLogger(__name__)


async def parse_chat(client: Client, chat: str) -> AsyncGenerator[Dict[str, Any], None]:
    gift_mappings = await gifts_list()
    logger.info(f"Starting parse for {chat}, loaded {len(gift_mappings)} gift mappings")

    try:
        chat_info = await client.get_chat(chat)
        member_count = chat_info.members_count or 0

        parser = parse_large_chat if member_count > 11000 else parse_regular_chat
        logger.info(f"Chat {chat} has {member_count} members, using appropriate parser")

        async for result in parser(client, chat, gift_mappings):
            yield result

    except Exception as e:
        logger.error(f"Error determining chat size for {chat}: {e}")
        async for result in parse_regular_chat(client, chat, gift_mappings):
            yield result


async def parse_large_chat(client: Client, chat: str, gift_mappings: Dict) -> AsyncGenerator[Dict[str, Any], None]:
    processed_users: Set[int] = set()
    total_processed = 0
    queries = [""] + [str(i) for i in range(10)] + list(ascii_lowercase)
    batch_gifts = []
    last_yield_count = 0

    try:
        peer = await client.resolve_peer(chat)

        for query in queries:
            offset = 0
            limit = 200

            while True:
                try:
                    participants = await client.invoke(
                        raw.functions.channels.GetParticipants(
                            channel=peer,
                            filter=raw.types.ChannelParticipantsSearch(q=query),
                            offset=offset,
                            limit=limit,
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

                batch_size = 300
                for i in range(0, len(new_users), batch_size):
                    user_batch = new_users[i:i + batch_size]

                    tasks = []
                    for user in user_batch:
                        processed_users.add(user.id)
                        total_processed += 1
                        tasks.append(process_user_gifts(client, user.id, user.username, gift_mappings))

                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    for result in results:
                        if isinstance(result, list) and result:
                            batch_gifts.extend(result)

                    if total_processed - last_yield_count >= 300:
                        logger.info(f"Progress: {total_processed} users processed, {len(batch_gifts)} gifts found")
                        yield {"gifts": batch_gifts, "total_processed": total_processed}
                        batch_gifts = []
                        last_yield_count = total_processed

                offset += len(participants.participants)

                if offset > 10000:
                    break

        if batch_gifts or total_processed != last_yield_count:
            yield {"gifts": batch_gifts, "total_processed": total_processed}

        logger.info(f"Completed parsing {chat}: {total_processed} users processed")

    except Exception as e:
        logger.error(f"Error parsing {chat}: {e}")


async def parse_regular_chat(client: Client, chat: str, gift_mappings: Dict) -> AsyncGenerator[Dict[str, Any], None]:
    total_processed = 0
    batch_gifts = []
    last_yield_count = 0
    current_batch = []
    batch_size = 500

    try:
        async for member in client.get_chat_members(chat, filter=ChatMembersFilter.SEARCH):
            if not member.user or member.user.is_bot:
                continue

            current_batch.append(member)

            if len(current_batch) >= batch_size:
                tasks = []
                for m in current_batch:
                    total_processed += 1
                    tasks.append(process_user_gifts(client, m.user.id, m.user.username, gift_mappings))

                results = await asyncio.gather(*tasks, return_exceptions=True)

                for result in results:
                    if isinstance(result, list) and result:
                        batch_gifts.extend(result)

                current_batch = []

                if total_processed - last_yield_count >= batch_size:
                    logger.info(f"Progress: {total_processed} users processed, {len(batch_gifts)} gifts found")
                    yield {"gifts": batch_gifts, "total_processed": total_processed}
                    batch_gifts = []
                    last_yield_count = total_processed

        if current_batch:
            tasks = []
            for m in current_batch:
                total_processed += 1
                tasks.append(process_user_gifts(client, m.user.id, m.user.username, gift_mappings))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, list) and result:
                    batch_gifts.extend(result)

        if batch_gifts or total_processed != last_yield_count:
            yield {"gifts": batch_gifts, "total_processed": total_processed}

    except Exception as e:
        logger.error(f"Error parsing {chat}: {e}")


async def process_user_gifts(client: Client, user_id: int, username: str, gift_mappings: Dict) -> List[Dict[str, Any]]:
    user_gifts = []
    try:
        peer = await client.resolve_peer(user_id)

        r = await client.invoke(
            raw.functions.payments.GetSavedStarGifts(
                peer=peer,
                offset="",
                limit=100,
                exclude_unlimited=True,
                exclude_unique=True,
                exclude_saved=None,
                exclude_unsaved=None,
                sort_by_value=None
            ),
            sleep_threshold=60
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        received_gifts = [
            await types.ReceivedGift._parse(client, gift, users, chats)
            for gift in r.gifts
        ]

        for gift in received_gifts:
            if gift.gift and str(gift.gift.id) in gift_mappings:
                user_gifts.append({
                    "gift": str(gift.gift.id),
                    "gift_name": gift_mappings[str(gift.gift.id)],
                    "user_id": user_id,
                    "username": username or ""
                })

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception:
        pass

    return user_gifts
