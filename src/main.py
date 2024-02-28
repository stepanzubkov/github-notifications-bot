
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.utils.formatting import Text, Bold, as_list

from config import settings
from database import crud
from database.core import init
from services.notifications import get_notifications_by_access_token, updated_at_to_formatted_timedelta

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


@dp.message(Command("notifications"))
async def command_notifications(message: types.Message):
    user_id = message.from_user.id
    user = await crud.user.get_user_by_user_id(user_id=user_id)
    if user is None:
        await message.reply("Сначала зарегестрируйтесь с помощью команды /login")
        return
    notifications = get_notifications_by_access_token(access_token=user.gh_access_token, since=user.last_checked)
    await crud.user.update_last_checked_by_user_id(user_id=user_id)
    if notifications.totalCount == 0:
        await message.reply("Нет новых уведомлений!")
        return
    content = as_list(
        Text("Уведомления:"),
        *[Text(Bold(n.subject.title), f" - {updated_at_to_formatted_timedelta(n.updated_at)}")
          for n in notifications]
    )
    await message.reply(**content.as_kwargs())


async def main() -> None:
    bot = Bot(settings.bot_token)
    await init()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
