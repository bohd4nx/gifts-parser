from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.states import ParseStates

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    try:
        await message.delete()
    except Exception:
        pass

    await state.clear()

    start_text = (
        "<b>👋 Hello {}!</b>\n\n"
        "<b>ℹ️ Important Information:</b>\n"
        "• I can only parse <b>public groups</b>\n"
        "• Groups must have <b>visible members list</b>\n"
        "• Private groups and channels are <b>not supported</b>\n"
        "• Large groups may take some time to process\n\n"
        "<b>📝 How to use:</b>\n"
        "1. Send me a public group link (e.g., @groupname or https://t.me/groupname)\n"
        "2. Wait for the parsing process to complete\n"
        "3. Download the results file\n\n"
        "<b>⚠️ Limitations:</b>\n"
        "• Cannot parse private groups\n"
        "• Cannot parse groups with hidden members\n"
        "• Rate limits may apply\n\n"
        "<b>🚀 Ready to start? Send me a group link!</b>\n\n"
        "<b>Made with ❤️ by @B7XX7B</b>"
    ).format(message.from_user.first_name)

    del_msg = await message.answer(text=start_text)
    await state.set_data({"del_msg": del_msg})
    await state.set_state(ParseStates.waiting_for_link)
