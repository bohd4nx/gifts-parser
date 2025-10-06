import logging
from typing import Dict

import aiohttp


async def gifts_list() -> Dict[str, str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cdn.changes.tg/gifts/id-to-name.json", ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                return {}
    except Exception as e:
        logging.error(f"Error fetching gifts: {e}")
        return {}
