import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict

import aiohttp

GIFTS_API_URL = "https://cdn.changes.tg/gifts/id-to-name.json"
CACHE_DURATION = timedelta(hours=1)


class GiftsManager:
    _instance = None
    _cache: Dict[str, str] = {}
    _last_update: datetime = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GiftsManager, cls).__new__(cls)
        return cls._instance

    @property
    def cache_expired(self) -> bool:
        return (
                self._last_update is None or
                datetime.now() - self._last_update > CACHE_DURATION
        )

    async def _fetch_and_update_cache(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(GIFTS_API_URL, ssl=False) as response:
                    if response.status == 200:
                        self._cache = await response.json()
                        self._last_update = datetime.now()
        except Exception as e:
            logging.error(f"Error fetching gifts: {e}")
            if not self._cache:
                self._cache = {}
                self._last_update = datetime.now()

    async def get_mappings(self) -> Dict[str, str]:
        if self.cache_expired:
            await self._fetch_and_update_cache()
        return self._cache


gifts_manager = GiftsManager()


def _init_cache():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    return loop.run_until_complete(gifts_manager.get_mappings())


GIFT_MAPPINGS = _init_cache()
