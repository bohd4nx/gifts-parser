import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from bot.services.saver import FileService
from bot.settings import GiftParser
from bot.states import ParseStates
from bot.utils.formatter import format_time_duration
from bot.utils.texts import (
    get_batch_info,
    get_error_next,
    get_status_message,
    get_final_message,
    get_final_batch_message,
    INIT_TEXT,
    get_button_text,
    get_error_text
)
from data.config import ADMINS

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
    start_time: datetime = None

    def __post_init__(self):
        self.start_time = datetime.now()

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

    def get_eta(self) -> str:
        if not self.start_time or self.parsed_count == 0:
            return "🤷‍♂️"

        elapsed = (datetime.now() - self.start_time).total_seconds()
        speed = self.parsed_count / elapsed
        remaining = self.total_members - self.parsed_count
        eta_seconds = remaining / speed if speed > 0 else 0

        return format_time_duration(eta_seconds)

    def get_elapsed_time(self) -> str:
        if not self.start_time:
            return "0с"
        return format_time_duration((datetime.now() - self.start_time).total_seconds())


class ParseManager:
    def __init__(self):
        self.file_service = FileService()
        self.parser = GiftParser()
        self.active_session: ParseSession = None
        self._status_task = None

    async def _update_status_loop(self, session: ParseSession):
        while not session.is_completed:
            await self.update_status(session)
            await asyncio.sleep(1)

    def create_session(self, chat: str, status_message: Message) -> ParseSession:
        if self._status_task:
            self._status_task.cancel()

        self.active_session = ParseSession(
            chat=chat,
            status_message=status_message,
            last_update=datetime.now()
        )

        self._status_task = asyncio.create_task(self._update_status_loop(self.active_session))
        return self.active_session

    async def stop_session(self):
        if self._status_task:
            self._status_task.cancel()
            self._status_task = None

        if self.active_session:
            elapsed_time = self.active_session.get_elapsed_time()
            percent = round((self.active_session.parsed_count / self.active_session.total_members * 100),
                            1) if self.active_session.total_members > 0 else 0

            final_text = get_final_message(
                chat=self.active_session.chat,
                total=self.active_session.total_members,
                processed=self.active_session.parsed_count,
                found=self.active_session.found_users,
                percent=percent,
                elapsed=elapsed_time,
                stopped=self.active_session.stop_requested
            )

            keyboard = self.get_keyboard(is_parsing=False,
                                         chat=self.active_session.chat) if self.active_session.found_users > 0 else None

            await self.active_session.status_message.edit_text(final_text, reply_markup=keyboard)

    @staticmethod
    def get_keyboard(is_parsing: bool = True, chat: str = None) -> InlineKeyboardMarkup:
        if is_parsing:
            return InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text=get_button_text('stop_parsing'),
                    callback_data="stop_parse"
                )
            ]])
        if chat:
            return InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text=get_button_text('download_results'),
                    callback_data=f"download_{chat}"
                )
            ]])
        return None

    async def update_status(self, session: ParseSession, show_stop: bool = True, batch_info: str = '') -> None:
        if not session.should_update_status():
            return

        percent = round((session.parsed_count / session.total_members * 100), 1) if session.total_members > 0 else 0
        status_text = get_status_message(
            chat=session.chat,
            total=session.total_members,
            processed=session.parsed_count,
            found=session.found_users,
            percent=percent,
            eta=session.get_eta(),
            batch_info=batch_info
        )

        keyboard = self.get_keyboard(is_parsing=show_stop)
        await session.status_message.edit_text(status_text, reply_markup=keyboard)
        session.last_update = datetime.now()

    async def process_results(self, result: dict) -> None:
        if not result or not self.active_session:
            return

        if self.active_session.result_file is None:
            self.active_session.result_file = self.file_service.get_unique_filename(self.active_session.chat)

        self.active_session.found_users = result.get("total_found", self.active_session.found_users)
        self.active_session.parsed_count = result.get("total_processed", self.active_session.parsed_count)

        gifts = result["gifts"]
        gifts_by_user = {}
        for gift in gifts:
            user_id = gift['user_id']
            if user_id not in gifts_by_user:
                gifts_by_user[user_id] = {
                    'username': gift['username'],
                    'gifts': []
                }
            gifts_by_user[user_id]['gifts'].append(gift)

        for user_id, user_data in gifts_by_user.items():
            self.file_service.process(
                self.active_session.result_file,
                user_data['gifts'],
                user_data['username'],
                user_id
            )


parse_manager = ParseManager()


@router.callback_query(lambda c: c.data == "stop_parse")
async def stop_parse_callback(callback_query: CallbackQuery, state: FSMContext):
    if not parse_manager.active_session:
        await callback_query.answer(get_error_text('nothing_to_stop'), show_alert=True)
        return

    parse_manager.active_session.stop_requested = True
    await parse_manager.stop_session()
    await callback_query.answer("Парсинг остановлен")
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

    links = [link.strip() for link in message.text.split('\n') if link.strip()]
    if not links:
        return

    status_msg = await message.answer(INIT_TEXT)
    batch_info = get_batch_info(1, len(links)) if len(links) > 1 else ''

    for i, link in enumerate(links, 1):
        chat = link.replace('https://', '').replace('t.me/', '').replace('@', '').strip()
        session = parse_manager.create_session(chat, status_msg)

        try:
            session.total_members = await parse_manager.parser.get_total_members(chat)
            if session.total_members == 0:
                await status_msg.edit_text(get_error_text('cant_get_members'))
                if len(links) > 1:
                    await asyncio.sleep(3)
                    await status_msg.edit_text(get_error_next())
                continue

            if len(links) > 1:
                batch_info = get_batch_info(i, len(links))

            await parse_manager.update_status(session, batch_info=batch_info)

            async for result in parse_manager.parser.parse(chat):
                if session.should_stop():
                    break

                await parse_manager.process_results(result)

                if not session.stop_requested:
                    await parse_manager.update_status(session, show_stop=True, batch_info=batch_info)

        except Exception as e:
            logging.error(f"Parse error for {chat}: {e}")
            await status_msg.edit_text(get_error_text('parse_error', str(e)))
            if len(links) > 1:
                await asyncio.sleep(3)
                await status_msg.edit_text(get_error_next())
            continue
        finally:
            if session and not session.stop_requested:
                await parse_manager.stop_session()

        await asyncio.sleep(1)

    if len(links) > 1:
        await status_msg.edit_text("✅ " + get_final_batch_message())
    await state.set_state(ParseStates.waiting_for_link)


@router.callback_query(lambda c: c.data.startswith('download_'))
async def download_results(callback_query: CallbackQuery):
    chat = callback_query.data.replace('download_', '')

    file_path = None
    if parse_manager.active_session and parse_manager.active_session.chat == chat:
        file_path = parse_manager.active_session.result_file

    if not file_path or not os.path.exists(file_path):
        await callback_query.answer(get_error_text('results_not_found'), show_alert=True)
        return

    try:
        filename = os.path.basename(file_path)
        await callback_query.message.reply_document(
            FSInputFile(file_path, filename=filename)
        )
    except Exception as e:
        logging.error(f"Download error: {e}")
        await callback_query.answer(get_error_text('download_error'), show_alert=True)

    await callback_query.answer()
