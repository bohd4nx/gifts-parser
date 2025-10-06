from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from bot.keyboards import get_language_keyboard

router = Router(name=__name__)


@router.callback_query(F.data == "lang_en")
async def set_english_callback(callback: CallbackQuery, i18n: I18nContext):
    i18n.locale = "en"
    await callback.answer(i18n.get("alert-lang-changed-en"), show_alert=True)
    await callback.message.edit_text(
        i18n.get('start-text', name=callback.from_user.first_name),
        reply_markup=get_language_keyboard(i18n)
    )


@router.callback_query(F.data == "lang_ru")
async def set_russian_callback(callback: CallbackQuery, i18n: I18nContext):
    i18n.locale = "ru"
    await callback.answer(i18n.get("alert-lang-changed-ru"), show_alert=True)
    await callback.message.edit_text(
        i18n.get('start-text', name=callback.from_user.first_name),
        reply_markup=get_language_keyboard(i18n)
    )
