from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.states import ParseStates

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await message.delete()

    del_msg = await message.answer(
        text=f'<b>👋 Hello {message.from_user.first_name}! I am a gift parser bot. '
             f'Please send me a chat link to start parsing.</b>'
    )

    await state.update_data(del_msg=del_msg)
    await state.set_state(ParseStates.waiting_for_link)
