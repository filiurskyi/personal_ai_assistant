from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def keyboard_selector(state):
    state_data = await state.get_data()
    state_name = await state.get_state()
    if (
        state_name == "States:adding_event_json"
        or state_name == "States:adding_note_json"
        or state_name == "States:delete_screenshot"
    ):
        keyboard = cancel()
    elif state_name == "States:find_screenshot":
        keyboard = screenshots()
    else:
        keyboard = core_kb()

    return keyboard.as_markup(resize_keyboard=True)


def core_kb() -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Write new event")
    kb.button(text="Show all events")
    kb.button(text="Write new note")
    kb.button(text="Show all notes")
    kb.button(text="Add screenshot")
    kb.button(text="Find screenshot")
    kb.adjust(2)
    return kb


def screenshots() -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Delete screenshot by id")
    kb.attach(cancel())
    kb.adjust(1)
    return kb


def cancel() -> ReplyKeyboardBuilder:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Cancel")
    kb.adjust(1)
    return kb
