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