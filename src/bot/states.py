from aiogram.fsm.state import State, StatesGroup


class ParseStates(StatesGroup):
    waiting_for_link = State()
