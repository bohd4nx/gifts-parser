import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_runtime_core import FluentRuntimeCore
from pyrogram import Client, enums
from pyrogram.errors import AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked

from bot.core import logger, setup_logging, config
from bot.handlers import user, start


async def main() -> None:
    setup_logging()

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    client = Client(
        name=f"{config.PHONE_NUMBER}",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        phone_number=config.PHONE_NUMBER,
        system_version="Windows 11 x64 (24H2)",
        lang_pack="tdesktop",
        lang_code="en",
        workdir=str(Path(__file__).parent),
        client_platform=enums.ClientPlatform.DESKTOP,
        sleep_threshold=30,
        max_concurrent_transmissions=10
    )

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="locales/{locale}/LC_MESSAGES"
        ),
        default_locale=config.LOCALE.lower()
    )

    dp = Dispatcher()

    async with client as app:
        user.create_handler(app)

        dp.include_router(start.router)
        dp.include_router(user.router)

        i18n_middleware.setup(dispatcher=dp)

        await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (AuthKeyUnregistered, AuthKeyDuplicated, SessionRevoked):
        logger.error("Session authorization error. Please delete the session file as it is no longer valid.")
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    except Exception as ex:
        logger.error(f"Unexpected error: {str(ex)}")
