from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    adding_event_json = State()
    adding_note_json = State()
    find_screenshot = State()
