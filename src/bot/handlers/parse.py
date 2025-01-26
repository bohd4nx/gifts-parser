import asyncio
import logging
import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import ADMINS
from src.bot.parser import GiftParser
from src.bot.services.file_service import FileService
from src.bot.states import ParseStates

router = Router()
file_service = FileService()
gift_parser = GiftParser()


class ParseHandler:
    def __init__(self):
        pass

    @staticmethod
    async def update_status(msg: Message, chat: str, total: int, parsed: int, found: int) -> None:
        status_text = (
            f"🔍 <b>Parsing chat: @{chat}</b>\n\n"
            f"📊 <b>Total members:</b> {total}\n"
            f"⏳ <b>Parsed:</b> {parsed}/{total}\n"
            f"✨ <b>Found users:</b> {found}"
        )
        await msg.edit_text(status_text)


@router.message(ParseStates.waiting_for_link, F.from_user.id.in_(ADMINS))
async def parse_handler(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    await data["del_msg"].delete()
    await state.clear()

    chat = message.text.replace('https://', '').replace('t.me/', '').replace('@', '')
    status_msg = await message.answer("Initializing parse process...")

    total_chat_members = 0
    total_parsed = 0
    found_users = 0

    try:
        total_chat_members = await gift_parser.get_total_members(chat)
        await ParseHandler.update_status(status_msg, chat, total_chat_members, total_parsed, found_users)

        async for result_gift in gift_parser.parse(chat):
            total_parsed += 1

            if result_gift:
                found_users += 1
                user_info = result_gift[0]
                file_service.process(chat, result_gift, user_info['username'], user_info['user_id'])

            if total_parsed % 10 == 0 or result_gift:
                await ParseHandler.update_status(status_msg, chat, total_chat_members, total_parsed, found_users)

            await asyncio.sleep(0.5)

    except Exception as e:
        logging.error(f"Parse error: {e}")
        await message.answer(f"Error occurred: {str(e)}")

    finally:
        final_text = (
            f"✅ <b>Parse completed for @{chat}</b>\n\n"
            f"📊 <b>Total members:</b> {total_chat_members}\n"
            f"⏳ <b>Parsed:</b> {total_parsed}/{total_chat_members}\n"
            f"✨ <b>Found users:</b> {found_users}"
        )

        if found_users > 0:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📥 Download Results", callback_data=f"download_{chat}")]
            ])
            await status_msg.edit_text(final_text, reply_markup=keyboard)
        else:
            await status_msg.edit_text(final_text)


@router.callback_query(lambda c: c.data.startswith('download_'))
async def download_results(callback_query: CallbackQuery):
    chat = callback_query.data.replace('download_', '')
    file_path = file_service.get_results_path(chat)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        await callback_query.message.answer_document(
            FSInputFile(file_path, filename=f'{chat}_results.txt')
        )
    else:
        await callback_query.answer("No results found", show_alert=True)

    await callback_query.answer()
