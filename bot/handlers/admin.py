import logging
import os
import uuid

from aiogram import Bot, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message, CallbackQuery
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
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
        "Replying with web link: https://t.me/personalassistant_ai_bot/dashboard",
        reply_markup=keyboard,
    )
    



# @router.callback_query()
@router.message(Command("test"))
async def command_test_handler(message: Message):
# async def command_test_handler(message: Message, state: FSMContext) -> None:
    # stt = await state.get_state()
    # msg = f"MSG from {message.from_user.id}\nCurrent state is : " + str(stt)
    # logging.info('CALLBACK LOL', query.data)
    builder = InlineKeyboardBuilder()
    builder.button(text="Нажми меня", callback_data="anything")
    args = message.get_url()
    print(args)
    await message.answer(
        text="Какой-то текст с кнопкой",
        reply_markup=builder.as_markup()
    )


@router.callback_query()
async def command_test_handler(query: CallbackQuery) -> None:
    # stt = await state.get_state()
    # msg = f"MSG from {message.from_user.id}\nCurrent state is : " + str(stt)
    print(query.data)


@router.callback_query(F.data == "anything")
async def callback_anything(callback: CallbackQuery):
    await callback.answer(
        text="Это какое-то обычное действие",
        show_alert=True
    )

