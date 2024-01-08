import asyncio
import logging
import os
import uuid

from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from aiogram.utils.chat_action import ChatActionSender
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


@router.message(States.adding_note_json)  # user message must be json
async def add_new_note_a_handler(message: Message, state: FSMContext, session, bot: Bot) -> None:
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        keyboard = await kb.keyboard_selector(state)
        await asyncio.sleep(0.01)
        gpt_answer = gpt.text_to_text(message.text, "create_new_note")
        answer = await f.user_context_handler(gpt_answer, message.from_user.id, session)
        await state.clear()
        keyboard = await kb.keyboard_selector(state)
        await message.answer(answer, reply_markup=keyboard, parse_mode=ParseMode.HTML)
