#!/usr/bin/env python3
import asyncio
import logging
import sys
from os import getenv

import uvicorn
from aiogram import Bot, Dispatcher  # , Router, types
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from bot.handlers import user_commands, admin, events, notes, screenshots, error
from bot.middlewares.db import DbSessionMiddleware
from db.conf import DB_URI

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def scheduler():
    while True:
        await asyncio.sleep(60)
        logging.info("scheduled 60 sec task...")


async def run_uvicorn():
    ...
    # config = uvicorn.Config("fastapi_app.main:app", port=8000, log_level="info")
    # server = uvicorn.Server(config)
    # await server.serve()


async def main() -> None:
    engine = create_async_engine(DB_URI, echo=False)
    sessionmaker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.include_routers(user_commands.router) #  must be at begin
    dp.include_routers(admin.router)
    dp.include_routers(events.router)
    dp.include_routers(notes.router)
    dp.include_routers(screenshots.router)
    dp.include_routers(error.router) #  must be at the end

    tasks = [dp.start_polling(bot), scheduler(), run_uvicorn()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("KeyboardInterrupt: ", e)
