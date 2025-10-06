from aiogram import Router, F
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.handlers.parser import process_chat_parsing
from bot.utils import validate_chat, parse_chat_link, format_number, is_large_chat

router = Router(name=__name__)


def create_handler(client):
    @router.message(F.text.regexp(r'@\w+|https?://t\.me/\w+'))
    async def handle_link(message: Message, i18n: I18nContext):
        chat_username = parse_chat_link(message.text)

        is_valid, error_msg, member_count = await validate_chat(message.bot, chat_username, i18n)
        if not is_valid:
            await message.reply(error_msg)
            return

        progress_key = 'parsing-started-large' if is_large_chat(member_count) else 'parsing-started'
        progress_message = await message.reply(
            i18n.get(progress_key, chat=chat_username, total=format_number(member_count)))

        await process_chat_parsing(
            client,
            message,
            i18n,
            chat_username,
            member_count,
            progress_message
        )

    return handle_link
