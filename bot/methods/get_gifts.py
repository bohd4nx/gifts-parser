import asyncio
from typing import Dict, Any, List

from pyrogram import Client, types
from pyrogram import raw
from pyrogram.errors import FloodWait

GIFTS_LIMIT = 100
SLEEP_THRESHOLD = 30


async def get_user_gifts(client: Client, user_id: int, username: str, gift_mappings: Dict) -> List[Dict[str, Any]]:
    user_gifts = []
    try:
        peer = await client.resolve_peer(user_id)

        r = await client.invoke(
            raw.functions.payments.GetSavedStarGifts(
                peer=peer,
                offset="",
                limit=GIFTS_LIMIT,
                exclude_unlimited=True,
                exclude_unique=True,
                exclude_saved=None,
                exclude_unsaved=None,
                sort_by_value=None
            ),
            sleep_threshold=SLEEP_THRESHOLD
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        received_gifts = [
            await types.ReceivedGift._parse(client, gift, users, chats)
            for gift in r.gifts
        ]

        for received_gift in received_gifts:
            if received_gift.gift and hasattr(received_gift.gift, 'id') and str(received_gift.gift.id) in gift_mappings:
                user_gifts.append({
                    "gift": str(received_gift.gift.id),
                    "gift_name": gift_mappings[str(received_gift.gift.id)],
                    "user_id": user_id,
                    "username": username or ""
                })

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception:
        pass

    return user_gifts
