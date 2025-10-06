import re

from aiogram import Bot
from aiogram_i18n import I18nContext


def parse_chat_link(text: str) -> str:
    if text.startswith('@'):
        return text

    match = re.search(r't\.me/([\w_]+)', text)
    if match:
        return f"@{match.group(1)}"

    return text


def format_number(num: int) -> str:
    return f"{num:,}".replace(",", ".")


async def validate_chat(bot: Bot, chat: str, i18n: I18nContext) -> tuple[bool, str, int]:
    try:
        chat_info = await bot.get_chat(chat)
        member_count = await bot.get_chat_member_count(chat)

        if hasattr(chat_info, 'has_hidden_members') and chat_info.has_hidden_members:
            return False, i18n.get('hidden-members', chat=chat), 0

        return True, "", member_count

    except Exception:
        return False, i18n.get('cant-get-members', chat=chat), 0
