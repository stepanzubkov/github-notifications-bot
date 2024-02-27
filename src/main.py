
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart, Command

from config import settings
from database import crud
from database.core import init

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("Привет")


@dp.message(Command("login"))
async def command_login(message: types.Message, command: CommandObject):
    if command.args is None or " " in command.args:
        await message.reply("Токен доступа не должен содержать пробелов.")
        return

    gh_access_token = command.args
    user_id = message.from_user.id

    await crud.user.create_or_update_user(user_id=user_id, gh_access_token=gh_access_token)
    await message.reply("Вы успешно вошли в аккаунт!")


async def main() -> None:
    bot = Bot(settings.bot_token)
    await init()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
