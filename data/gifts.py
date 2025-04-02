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

# ╔════════════════════════════════════════════════════════╗
# ║                                                        ║
# ║          Comment the code above and uncomment the      ║
# ║          part below if you only want specific gifts.   ║
# ║                                                        ║
# ║                    Made by @bohd4nx                    ║
# ╚════════════════════════════════════════════════════════╝

# GIFT_MAPPINGS = {
#   "5983471780763796287": "Santa Hat",
#   "5936085638515261992": "Signet Ring",
#   "5933671725160989227": "Precious Peach",
#   "5936013938331222567": "Plush Pepe",
#   "5913442287462908725": "Spiced Wine",
#   "5915502858152706668": "Jelly Bunny",
#   "5915521180483191380": "Durov's Cap",
#   "5913517067138499193": "Perfume Bottle",
#   "5882125812596999035": "Eternal Rose",
#   "5882252952218894938": "Berry Box",
#   "5857140566201991735": "Vintage Cigar",
#   "5846226946928673709": "Magic Potion",
#   "5845776576658015084": "Kissed Frog",
#   "5825801628657124140": "Hex Pot",
#   "5825480571261813595": "Evil Eye",
#   "5841689550203650524": "Sharp Tongue",
#   "5841391256135008713": "Trapped Heart",
#   "5839038009193792264": "Skull Flower",
#   "5837059369300132790": "Scared Cat",
#   "5821261908354794038": "Spy Agaric",
#   "5783075783622787539": "Homemade Cake",
#   "5933531623327795414": "Genie Lamp",
#   "6028426950047957932": "Lunar Snake",
#   "6003643167683903930": "Party Sparkler",
#   "5933590374185435592": "Jester Hat",
#   "5821384757304362229": "Witch Hat",
#   "5915733223018594841": "Hanging Star",
#   "5915550639663874519": "Love Candle",
#   "6001538689543439169": "Cookie Heart",
#   "5782988952268964995": "Desk Calendar",
#   "6001473264306619020": "Jingle Bells",
#   "5980789805615678057": "Snow Mittens",
#   "5836780359634649414": "Voodoo Doll",
#   "5841632504448025405": "Mad Pumpkin",
#   "5825895989088617224": "Hypno Lollipop",
#   "5782984811920491178": "B-Day Candle",
#   "5935936766358847989": "Bunny Muffin",
#   "5933629604416717361": "Astral Shard",
#   "5837063436634161765": "Flying Broom",
#   "5841336413697606412": "Crystal Ball",
#   "5821205665758053411": "Eternal Candle",
#   "5936043693864651359": "Swiss Watch",
#   "5983484377902875708": "Ginger Cookie",
#   "5879737836550226478": "Mini Oscar",
#   "5170594532177215681": "Lol Pop",
#   "5843762284240831056": "Ion Gem",
#   "5936017773737018241": "Star Notepad",
#   "5868659926187901653": "Loot Bag",
#   "5868348541058942091": "Love Potion",
#   "5868220813026526561": "Toy Bear",
#   "5868503709637411929": "Diamond Ring",
#   "5167939598143193218": "Sakura Flower",
#   "5981026247860290310": "Sleigh Bell",
#   "5897593557492957738": "Top Hat",
#   "5856973938650776169": "Record Player",
#   "5983259145522906006": "Winter Wreath",
#   "5981132629905245483": "Snow Globe",
#   "5846192273657692751": "Electric Skull",
#   "6023752243218481939": "Tama Gadget",
#   "6003373314888696650": "Candy Cane",
#   "5933793770951673155": "Neko Helmet",
#   "6005659564635063386": "Jack-in-the-Box"
# }
