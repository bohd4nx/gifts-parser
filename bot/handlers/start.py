from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.states import ParseStates
from bot.utils import START_TEXT

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass

    await state.clear()
    del_msg = await message.answer(text=START_TEXT.format(name=message.from_user.first_name))
    await state.set_data({"del_msg": del_msg})
    await state.set_state(ParseStates.waiting_for_link)
