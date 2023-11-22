#!/usr/bin/env python3
import asyncio
import logging
import sys
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher  # , Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from handlers import user_commands

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
PG_PWD = getenv("PGPWD")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()


async def on_startup() -> None:
    """initialize db"""
    # await db.db_start_pl()
    # await db.db_start_gm()
    pass

    print("> BOT has been successfully started")


async def main() -> None:

    dp.include_routers(user_commands.router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
