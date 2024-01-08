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



@router.message(Command("chat_id"))
async def get_chat_id_handler(message: Message, state: FSMContext, session):
    print(message.chat.id)
    await message.answer(str(message.chat.id))


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
    