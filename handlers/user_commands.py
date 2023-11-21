from aiogram import Router, F, types
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold
from logic.states import States
import keyboards.kb as kb
# from logic import aichat as gpt
# from datetime import datetime
from logic.calendar import generate_ics_file
from pathlib import Path

import logging 


# from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
router = Router()

@router.message(Command("state"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    logging.info(await state.get_state())


@router.message(Command("get"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    file = FSInputFile(generate_ics_file())
    await message.answer_document(document=file)

@router.message(F.text == "Add new event")
async def add_new_event_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    await state.set_state(States.asked_for_date)
    await message.answer("Enter Event Date!", reply_markup=keyboard)


@router.message(States.asked_for_date)
async def add_new_date_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer("Enter Event Time!", reply_markup=keyboard)
    await state.set_state(States.asked_for_time)


@router.message(States.asked_for_time)
async def ask_for_date_handler(message: types.Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    await message.answer(
        f"Received message:\n{message.text}", reply_markup=keyboard
    )


@router.message(F.text == "Show all events")
async def show_all_events_handler(message: Message, state: FSMContext) -> None:
    keyboard = await kb.keyboard_selector(state)
    # answer = gpt.simplequery()
    answer = "simple answer"
    await message.answer(answer, reply_markup=keyboard)


@router.message(F.voice)
async def voice_messages_handler(message: Message, state: FSMContext) -> None:
    # answer = gpt.voice_to_text(message.voice)
    answer = "simple answer2"
    keyboard = await kb.keyboard_selector(state)
    await message.answer(answer, reply_markup=keyboard)    


@router.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    
    keyboard = await kb.keyboard_selector(state)
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=keyboard
    )

