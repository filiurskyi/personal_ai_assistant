from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def keyboard_selector(state):
    # state_data = await state.get_data()
    state_name = await state.get_state()
    if state_name == "State:":
        keyboard = None
    else:
        keyboard = core_kb()

    return keyboard.as_markup(resize_keyboard=True)


def core_kb() -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Add new event")
    kb.button(text="Show all events")
    kb.adjust(2)
    return kb
