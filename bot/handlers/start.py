from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext

from bot.keyboards import get_language_keyboard

router = Router(name=__name__)


@router.message(CommandStart())
async def start_handler(message: Message, i18n: I18nContext):
    await message.answer(
        i18n.get('start-text', name=message.from_user.first_name),
        reply_markup=get_language_keyboard(i18n)
    )
