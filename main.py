import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from Register.handlers.user_crud import router1
from Register.handlers.start import router2
from Register.handlers.admin import admin_router
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher(storage=MemoryStorage())


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(router1)
    dp.include_router(router2)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())