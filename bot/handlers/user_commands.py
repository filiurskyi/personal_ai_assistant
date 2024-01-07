import logging
import os
import uuid

from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

import bot.keyboards.kb as kb
from bot.db_tools import database as db
from bot.logic import aichat as gpt
from bot.logic import reply_format as f
from bot.logic.calendar import generate_ics_file
from bot.logic.states import States
from bot.logic.utils import ocr_image

# from datetime import datetime


router = Router()


@router.message(States.adding_event_json, F.text == "Cancel")
async def cancel_adding_event_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    await state.clear()
    keyboard = await kb.keyboard_selector(state)
    answer = "Cancelled adding new event.\n\nI am your personal assistant."
    await message.answer(answer, reply_markup=keyboard)


@router.message(States.find_screenshot, F.text == "Cancel")
async def cancel_finding_screenshot_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    await state.clear()
    keyboard = await kb.keyboard_selector(state)
    answer = "Cancelled searching for screenshots.\n\nI am your personal assistant."
    await message.answer(answer, reply_markup=keyboard)


@router.message(States.delete_screenshot, F.text == "Cancel")
async def cancel_finding_screenshot_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    await state.clear()
    keyboard = await kb.keyboard_selector(state)
    answer = "Cancelled deleting screenshots.\n\nI am your personal assistant."
    await message.answer(answer, reply_markup=keyboard)


@router.message(States.find_screenshot, F.text == "Delete screenshot by id")
async def cancel_finding_screenshot_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    keyboard = await kb.keyboard_selector(state)
    await state.set_state(States.delete_screenshot)
    await message.answer(
        "Now send my id of screenshot you want to delete. It is in brackets like this: [id]",
        reply_markup=keyboard,
    )


@router.message(States.delete_screenshot)
async def cancel_finding_screenshot_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    await state.set_state(States.find_screenshot)
    keyboard = await kb.keyboard_selector(state)
    delete_successful = await db.delete_screenshot(
        session, message.from_user.id, message.text
    )
    if delete_successful:
        await message.answer(
            f"screenshot with id[{message.text}] deleted", reply_markup=keyboard
        )
    else:
        await message.answer(
            f"screenshot with id[{message.text}] not found", reply_markup=keyboard
        )


@router.message(States.adding_note_json, F.text == "Cancel")
async def cancel_adding_note_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    await state.clear()
    keyboard = await kb.keyboard_selector(state)
    answer = (
        "Cancelled adding new note.\n\nI am your personal assistant, i can create events and notes from your "
        "voice message, or you can manually add events or notes by buttons Write.. below your screen."
    )
    await message.answer(answer, reply_markup=keyboard)


@router.message(Command("state"))
async def command_state_handler(message: Message, state: FSMContext) -> None:
    stt = await state.get_state()
    msg = f"MSG from {message.from_user.id}\nCurrent state is : " + str(stt)
    logging.info(msg)


@router.message(Command("web"))
async def command_web_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer(
        "Replying with web link: https://t.me/personalassistant_ai_test_bot/dashboard",
        reply_markup=keyboard,
    )


@router.message(Command("get_ics"))
async def command_get_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    events_list = await db.show_all_events(session, message.from_user.id)
    default_event_duration = await db.get_user_default_event_duration(
        session, message.from_user.id
    )
    file_path = generate_ics_file(events_list, default_event_duration)
    file = FSInputFile(file_path)
    await message.answer_document(document=file, reply_markup=keyboard)
    os.remove(file_path)


@router.message(Command("help"))
async def command_help_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    msg = (
        "/start - log in\n/help - display help message\n\n/get_ics - download .ics calendar\nFor Apple users: https://routinehub.co/shortcut/7005/\n\n/del_all_events - delete "
        "all events\n\n/del_all_notes - delete all notes\n\n\n\n/state - for debugging"
    )
    await message.answer(msg, reply_markup=keyboard)


@router.message(F.text == "Write new event")
async def add_new_event_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(States.adding_event_json)
    keyboard = await kb.keyboard_selector(state)
    await message.answer("Enter your event description by text:", reply_markup=keyboard)


@router.message(F.text == "Write new note")
async def add_new_note_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(States.adding_note_json)
    keyboard = await kb.keyboard_selector(state)
    await message.answer("Enter your note description by text:", reply_markup=keyboard)


@router.message(States.adding_event_json, F.voice)
async def voice_messages_add_event_state_handler(
    message: Message, state: FSMContext, bot, session
) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer(
        "I am accepting only text in this mode. To use voice input press Cancel.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


@router.message(States.adding_note_json, F.voice)
async def voice_messages_add_note_state_handler(
    message: Message, state: FSMContext, bot, session
) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer(
        "I am accepting only text in this mode. To use voice input press Cancel.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


@router.message(States.adding_event_json)  # user message must be json
async def add_new_event_a_handler(message: Message, state: FSMContext, session) -> None:
    gpt_answer = gpt.text_to_text(message.text, "create_new_event")
    answer = await f.user_context_handler(gpt_answer, message.from_user.id, session)
    await state.clear()
    keyboard = await kb.keyboard_selector(state)
    await message.answer(answer, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@router.message(States.adding_note_json)  # user message must be json
async def add_new_note_a_handler(message: Message, state: FSMContext, session) -> None:
    gpt_answer = gpt.text_to_text(message.text, "create_new_note")
    answer = await f.user_context_handler(gpt_answer, message.from_user.id, session)
    await state.clear()
    keyboard = await kb.keyboard_selector(state)
    await message.answer(answer, reply_markup=keyboard, parse_mode=ParseMode.HTML)


@router.message(States.find_screenshot)
async def find_screenshot_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    result = await db.find_screenshot(session, message.from_user.id, message.text)
    if len(result) != 0:
        for res in result:
            print(f"found photo with file_id == {res[0]=}")
            await message.answer_photo(
                res[1], caption=f"[{res[0]}]\nhere is your photo", reply_markup=keyboard
            )
            # await message.answer(result, reply_markup=keyboard)
    else:
        await message.answer("found nothing...", reply_markup=keyboard)


@router.message(F.photo)
async def get_photo_handler(message: Message, state: FSMContext, session, bot) -> None:
    keyboard = await kb.keyboard_selector(state)
    file_id = await bot.get_file(message.photo[-1].file_id)
    file_path = f"./screenshots/{uuid.uuid4().int}.jpg"
    await bot.download_file(file_id.file_path, file_path)
    image = Image.open(file_path)
    caption = message.caption
    filtered_text = ocr_image(image)
    screenshot_id = await db.add_new_screenshot(
        session, message.from_user.id, file_id.file_id, caption, filtered_text
    )
    await message.answer(
        f"<i>[{screenshot_id}] Photo received with name: {file_path}</i>\nCaption is: {caption}\nText recognized:\n\n{filtered_text}",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )
    image.close()
    os.remove(file_path)


@router.message(F.text == "Show all events")
async def show_all_events_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    events = await db.show_all_events(session, message.from_user.id)
    if events:
        for event in events:
            ev = await f.display_event_card(event.id, session, message.from_user.id)
            await message.answer(ev, reply_markup=keyboard)
    else:
        await message.answer(
            "<i>No events found.</i>", reply_markup=keyboard, parse_mode=ParseMode.HTML
        )


@router.message(F.text == "Add screenshot")
async def add_screenshot_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer(
        "You can send me your screenshots anytime.", reply_markup=keyboard
    )


@router.message(F.text == "Find screenshot")
async def find_screenshot_handler(message: Message, state: FSMContext, session) -> None:
    await state.set_state(States.find_screenshot)
    keyboard = await kb.keyboard_selector(state)
    await message.answer("Enter text from screenshot:", reply_markup=keyboard)


@router.message(F.text == "Show all notes")
async def show_all_notes_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    notes = await db.show_all_notes(session, message.from_user.id)
    if notes:
        for note in notes:
            nt = await f.display_note_card(note.id, session, message.from_user.id)
            await message.answer(nt, reply_markup=keyboard)
    else:
        await message.answer(
            "<i>No notes found.</i>", reply_markup=keyboard, parse_mode=ParseMode.HTML
        )


@router.message(F.voice)
async def voice_messages_handler(
    message: Message, state: FSMContext, bot, session
) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer("Got you, pls w8...", reply_markup=keyboard)
    file_id = await bot.get_file(message.voice.file_id)
    file_path = f"./temp/{uuid.uuid4().int}.oga"
    await bot.download_file(file_id.file_path, file_path)
    audio = open(file_path, "rb")
    transcript = gpt.voice_to_text(audio)
    audio.close()
    answer = await f.user_context_handler(transcript, message.from_user.id, session)
    await message.answer(answer, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    os.remove(file_path)


@router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext, session) -> None:
    """
    This handler receives messages with `/start` command
    """
    keyboard = await kb.keyboard_selector(state)
    if not await db.old_user_check(session, message.from_user.id):
        await message.answer(
            f"Welcome back, {hbold(message.from_user.full_name)}!\nServer has been updated",
            reply_markup=keyboard,
        )
    else:
        await db.add_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.full_name,
        )
        await message.answer(
            f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=keyboard
        )


@router.message(Command("del_all_events"))
async def del_all_events_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    await db.delete_all_events(session, message.from_user.id)
    await message.answer(
        "<i>All events deleted.</i>", reply_markup=keyboard, parse_mode=ParseMode.HTML
    )


@router.message(Command("del_all_notes"))
async def del_all_notes_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    await db.del_all_notes(session, message.from_user.id)
    await message.answer(
        "<i>All events deleted.</i>", reply_markup=keyboard, parse_mode=ParseMode.HTML
    )


@router.message(F.text)
async def show_all_events_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    keyboard = await kb.keyboard_selector(state)
    answer = "Got message:\n" + message.text + "\n\nDoes nothing.."
    await message.answer(answer, reply_markup=keyboard)
