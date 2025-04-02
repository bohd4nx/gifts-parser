import asyncio
import logging
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from bot import BotCommands, router, get_client
from data.config import BOT_TOKEN


class TelegramBot:
    def __init__(self):
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.storage = MemoryStorage()
        self._configure_logging()

    @staticmethod
    def _configure_logging() -> None:
        logging.basicConfig(
            level=logging.ERROR,
            format='[%(asctime)s] - %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        dispatcher_logger = logging.getLogger('aiogram.dispatcher')
        dispatcher_logger.setLevel(logging.INFO)

    @staticmethod
    async def initialize_pyrogram() -> None:
        try:
            logging.info("Initializing Pyrogram session...")
            client = await get_client()
            if client and client.is_connected:
                logging.info(f"Pyrogram session initialized successfully: {client.me.first_name}")
            else:
                logging.error("Failed to initialize Pyrogram session")
        except Exception as e:
            logging.error(f"Error initializing Pyrogram: {e}")

    async def initialize(self) -> None:
        await self.initialize_pyrogram()

        self.bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode='HTML')
        )
        self.dp = Dispatcher(storage=self.storage)
        self.dp.include_router(router)
        await BotCommands.setup_commands(self.bot)

    async def start(self) -> None:
        try:
            await self.initialize()
            logging.info("Bot started")
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logging.error(f"Error starting bot: {e}")
            raise


async def main():
    bot_instance = TelegramBot()
    await bot_instance.start()


if __name__ == '__main__':
    asyncio.run(main())
