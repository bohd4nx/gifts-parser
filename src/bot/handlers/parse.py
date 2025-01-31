import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import ADMINS
from src.bot.parser import GiftParser
from src.bot.services.file_service import FileService
from src.bot.states import ParseStates

router = Router()


@dataclass
class ParseSession:
    chat: str
    total_members: int = 0
    parsed_count: int = 0
    found_users: int = 0
    stop_requested: bool = False
    status_message: Message = None
    last_update: datetime = None
    result_file: str = None

    @property
    def is_completed(self) -> bool:
        return self.parsed_count >= self.total_members or self.stop_requested

    def should_update_status(self, force: bool = False) -> bool:
        if not self.last_update:
            return True
        if force or self.parsed_count % 10 == 0:
            return True
        return (datetime.now() - self.last_update) > timedelta(seconds=1)

    def should_stop(self) -> bool:
        return self.stop_requested or self.parsed_count >= self.total_members


class ParseManager:
    def __init__(self):
        self.file_service = FileService()
        self.parser = GiftParser()
        self.active_session: ParseSession = None

    def create_session(self, chat: str, status_message: Message) -> ParseSession:
        self.active_session = ParseSession(
            chat=chat,
            status_message=status_message,
            last_update=datetime.now()
        )
        return self.active_session

    @staticmethod
    def get_keyboard(is_parsing: bool = True, chat: str = None) -> InlineKeyboardMarkup:
        if is_parsing:
            return InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="⏹ Stop Parsing", callback_data="stop_parse")
            ]])
        if chat:
            return InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="📥 Download Results", callback_data=f"download_{chat}")
            ]])
        return None

    async def update_status(self, session: ParseSession, show_stop: bool = True) -> None:
        if not session.should_update_status():
            return

        status_text = (
            f"🔍 <b>Parsing chat: @{session.chat}</b>\n\n"
            f"📊 <b>Total members:</b> {session.total_members}\n"
            f"⏳ <b>Parsed:</b> {session.parsed_count}/{session.total_members}\n"
            f"✨ <b>Found users:</b> {session.found_users}"
        )

        keyboard = self.get_keyboard(is_parsing=show_stop)
        await session.status_message.edit_text(status_text, reply_markup=keyboard)
        session.last_update = datetime.now()

    async def process_results(self, result_gift: dict) -> None:
        if not result_gift or not self.active_session:
            return

        if self.active_session.result_file is None:
            self.active_session.result_file = self.file_service.get_unique_filename(self.active_session.chat)

        self.active_session.found_users += 1
        user_info = result_gift[0]
        self.file_service.process(
            self.active_session.result_file,
            result_gift,
            user_info['username'],
            user_info['user_id']
        )


parse_manager = ParseManager()


@router.callback_query(lambda c: c.data == "stop_parse")
async def stop_parse_callback(callback_query: CallbackQuery, state: FSMContext):
    if not parse_manager.active_session:
        await callback_query.answer("No active parsing session")
        return

    parse_manager.active_session.stop_requested = True
    final_text = (
        f"🔍 <b>Parsing chat: @{parse_manager.active_session.chat}</b>\n\n"
        f"📊 <b>Total members:</b> {parse_manager.active_session.total_members}\n"
        f"⏳ <b>Parsed:</b> {parse_manager.active_session.parsed_count}/{parse_manager.active_session.total_members}\n"
        f"✨ <b>Found users:</b> {parse_manager.active_session.found_users}\n\n"
        f"⏹ <b>Parsing stopped by user</b>\n"
        f"✍️ Ready for next input"
    )

    keyboard = parse_manager.get_keyboard(is_parsing=False,
                                          chat=parse_manager.active_session.chat) if parse_manager.active_session.found_users > 0 else None

    await callback_query.message.edit_text(final_text, reply_markup=keyboard)
    await callback_query.answer("Parsing stopped")
    await state.set_state(ParseStates.waiting_for_link)


@router.message(ParseStates.waiting_for_link, F.from_user.id.in_(ADMINS))
async def parse_handler(message: Message, state: FSMContext):
    await message.delete()

    data = await state.get_data()
    if 'del_msg' in data:
        try:
            await data["del_msg"].delete()
        except Exception as e:
            logging.warning(f"Could not delete message: {e}")

    await state.clear()

    chat = message.text.replace('https://', '').replace('t.me/', '').replace('@', '').strip()
    init_text = (
        "🔄 <b>Initializing parse process...</b>\n\n"
        "<i>If initialization takes longer than expected, please check:</i>\n\n"
        "1️⃣ All dependencies are properly installed\n"
        "2️⃣ You have successfully logged in with your phone number\n"
        "3️⃣ Check console logs for any error messages\n\n"
        "❗️ If issues persist, please contact @B7XX7B for support\n\n"
        "<i>Please wait while we establish connection...</i>"
    )
    status_msg = await message.answer(init_text)
    session = parse_manager.create_session(chat, status_msg)

    try:
        session.total_members = await parse_manager.parser.get_total_members(chat)
        if session.total_members == 0:
            await status_msg.edit_text("❌ Failed to get members count. Make sure the group is public and accessible.")
            return

        await parse_manager.update_status(session)

        async for result_gift in parse_manager.parser.parse(chat):
            if session.should_stop():
                break

            session.parsed_count += 1
            await parse_manager.process_results(result_gift)

            if not session.stop_requested:
                await parse_manager.update_status(session)

    except Exception as e:
        logging.error(f"Parse error: {e}")
        await status_msg.edit_text(f"❌ Error occurred: {str(e)}")
    finally:
        if session and not session.stop_requested:
            final_text = (
                f"✅ <b>Parse completed for @{session.chat}</b>\n\n"
                f"📊 <b>Total members:</b> {session.total_members}\n"
                f"⏳ <b>Parsed:</b> {session.parsed_count}/{session.total_members}\n"
                f"✨ <b>Found users:</b> {session.found_users}\n\n"
                f"✍️ Ready for next input"
            )
            keyboard = parse_manager.get_keyboard(is_parsing=False,
                                                  chat=session.chat) if session.found_users > 0 else None
            await session.status_message.edit_text(final_text, reply_markup=keyboard)
            await state.set_state(ParseStates.waiting_for_link)


@router.callback_query(lambda c: c.data.startswith('download_'))
async def download_results(callback_query: CallbackQuery):
    chat = callback_query.data.replace('download_', '')

    file_path = None
    if parse_manager.active_session and parse_manager.active_session.chat == chat:
        file_path = parse_manager.active_session.result_file

    if not file_path or not os.path.exists(file_path):
        await callback_query.answer("Results not found", show_alert=True)
        return

    try:
        filename = os.path.basename(file_path)
        await callback_query.message.reply_document(
            FSInputFile(file_path, filename=filename)
        )
    except Exception as e:
        logging.error(f"Download error: {e}")
        await callback_query.answer("Error downloading results", show_alert=True)

    await callback_query.answer()
