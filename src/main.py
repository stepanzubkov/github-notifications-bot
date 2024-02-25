
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from config import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("Привет")


async def main() -> None:
    bot = Bot(settings.bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
