import logging
from typing import Dict

import aiohttp
from aiogram_i18n import I18nContext


def format_number(num: int) -> str:
    return f"{num:,}".replace(",", ".")


def format_time(i18n: I18nContext, seconds: float) -> str:
    is_hours = seconds >= 3600
    time_format_key = 'time-format-hours' if is_hours else 'time-format'

    if is_hours:
        time_params = {
            'hours': int(seconds // 3600),
            'minutes': int((seconds % 3600) // 60),
            'seconds': int(seconds % 60)
        }
    else:
        time_params = {
            'minutes': int(seconds // 60),
            'seconds': int(seconds % 60)
        }

    return i18n.get(time_format_key, **time_params)


def is_large_chat(member_count: int) -> bool:
    return member_count > 11000


async def fetch_gifts_list() -> Dict[str, str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cdn.changes.tg/gifts/id-to-name.json", ssl=False) as response:
                if response.status == 200:
                    return await response.json()
                return {}
    except Exception as e:
        logging.error(f"Error fetching gifts: {e}")
        return {}
