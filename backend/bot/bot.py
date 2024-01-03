#!/usr/bin/env python3
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher  # , Router, types
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from .handlers import user_commands
from .middlewares.db import DbSessionMiddleware

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
# PG_PWD = getenv("PG_PWD")
DB_URI = "sqlite+aiosqlite:///database.db/"
OPENAI_API_KEY = getenv("OPENAI_API_KEY")


async def scheduler():
    while True:
        await asyncio.sleep(60)
        logging.info("scheduled 60 sec task...")


async def main() -> None:
    engine = create_async_engine(DB_URI, echo=False)
    sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_routers(user_commands.router)

    tasks = [dp.start_polling(bot), scheduler()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
