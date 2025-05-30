import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
ADMINS = getenv('ADMINS')
dp = Dispatcher()


@dp.callback_query(F.data=='course_info')
async def callback_handler(callback_query):
      await callback_query.answer("Kurslar haqida ma'lumot beriladi", show_alert=True)


async def notify_startup(bot: Bot):
    await bot.send_message(ADMINS,'Bot ishga tushdi')

async def notify_shutdown(bot: Bot):
    await bot.send_message(ADMINS, 'Bot o\'chdi')


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
       await message.send_copy(chat_id=message.chat.id)
    except TypeError:
       await message.answer("Nice try")


async def main() -> None:
    from inline_bot_with_api.handlers import wiki_router, start_router

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(wiki_router, start_router)
    dp.startup.register(notify_startup)
    dp.shutdown.register(notify_shutdown)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
