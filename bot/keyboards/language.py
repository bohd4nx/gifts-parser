from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext


def get_language_keyboard(i18n: I18nContext) -> InlineKeyboardMarkup:
    en_text = i18n.get("btn-english") if i18n.locale != "en" else i18n.get("btn-english-selected")
    ru_text = i18n.get("btn-russian") if i18n.locale != "ru" else i18n.get("btn-russian-selected")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=en_text, callback_data="lang_en"),
                InlineKeyboardButton(text=ru_text, callback_data="lang_ru")
            ]
        ]
    )
    return keyboard
