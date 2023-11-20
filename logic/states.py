from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    asked_for_date = State()
    asked_for_time = State()
    asked_for_text = State()
