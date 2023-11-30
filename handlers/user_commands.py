import json
import logging
import os
import uuid

from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession

import keyboards.kb as kb
from db_tools import database as db
from logic import aichat as gpt
from logic import reply_format as f
from logic.calendar import generate_ics_file
from logic.states import States

# from datetime import datetime


router = Router()


@router.message(Command("state"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    msg = (
        f"MSG from {message.from_user.id}\nCurrent state is : "
        + await state.get_state()
    )
    logging.info(msg)


@router.message(Command("get_ics"))
async def command_get_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    events_list = await db.show_all_events(session, message.from_user.id)
    file_path = generate_ics_file(events_list)
    file = FSInputFile(file_path)
    await message.answer_document(document=file, reply_markup=keyboard)
    os.remove(file_path)


@router.message(Command("help"))
async def command_help_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    msg = (
        "/start - log in\n/help - display help message\n/get_ics - download .ics calendar\n/del_all_events - delete "
        "all saved events\n\n/state - debug"
    )
    await message.answer(msg, reply_markup=keyboard)


@router.message(F.text == "Add new event")
async def add_new_event_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    await state.set_state(States.asked_for_date)
    await message.answer("Enter JSON with event:", reply_markup=keyboard)


@router.message(States.asked_for_date)  # user message must be json
async def add_new_date_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    try:
        reply = await f.user_context_handler(
            message.text, message.from_user.id, session
        )
    except:
        reply = """Wrong input. Should be like:<code>
{
  "user_context": "create_new_event",
  "ev_title": "Заголовок",
  "ev_datetime": "03.12.2023 19:00",
  "ev_tags": "#tag1 #tag2",
  "ev_text": "Опис зустрічі"
}</code>"""
    await message.answer(reply, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    await state.clear()


@router.message(States.asked_for_time)
async def ask_for_date_handler(message: types.Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer(f"Received message:\n{message.text}", reply_markup=keyboard)


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


@router.message(F.voice)
async def voice_messages_handler(
    message: Message, state: FSMContext, bot, session
) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer("Got you, pls w8...", reply_markup=keyboard)
    file_id = await bot.get_file(message.voice.file_id)
    filename = f"./temp/{uuid.uuid4().int}.oga"
    await bot.download_file(file_id.file_path, filename)
    audio = open(filename, "rb")
    transcript = gpt.voice_to_text(audio)
    audio.close()
    answer = await f.user_context_handler(transcript, message.from_user.id, session)
    await message.answer(answer, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    os.remove(filename)


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
async def command_start_handler(message: Message, state: FSMContext, session) -> None:
    keyboard = await kb.keyboard_selector(state)
    await db.delete_all_events(session, message.from_user.id)
    await message.answer(
        "<i>All events deleted.</i>", reply_markup=keyboard, parse_mode=ParseMode.HTML
    )


@router.message(F.text)
async def show_all_events_handler(
    message: Message, state: FSMContext, bot: Bot, session: AsyncSession
) -> None:
    keyboard = await kb.keyboard_selector(state)
    answer = "Got message:\n" + message.text + "\n\nDoes nothing.."
    # await message.answer("running AI request")
    # answer = gpt.simple_query(message.text)
    await message.answer(answer, reply_markup=keyboard)
