#!/usr/bin/env python3
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher  # , Router, types
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from handlers import user_commands
from middlewares.db import DbSessionMiddleware

# from db_tools.models import Base

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
# PG_PWD = getenv("PG_PWD")
OPENAI_API_KEY = getenv("OPENAI_API_KEY")

# def database_init(engine) -> None:
#     Base.metadata.create_all(bind=engine)


async def main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///database.db/", echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    # dp.startup.trigger(database_init(engine))
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_routers(user_commands.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
