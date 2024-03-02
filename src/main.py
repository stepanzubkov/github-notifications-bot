
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandObject, CommandStart, Command, callback_data
from aiogram.utils.formatting import Text, Bold, as_list, TextLink

from config import settings
from database import crud
from database.core import init
from services.notifications import get_notifications_by_access_token, updated_at_to_formatted_timedelta, mark_notifications_as_read

dp = Dispatcher()

keyboard_reply = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[[KeyboardButton(text="/notifications")]],
)

class PlainCallback(callback_data.CallbackData, prefix="plain"):
    text: str

button_mark_as_read = InlineKeyboardButton(text="Пометить все как прочитанные", callback_data=PlainCallback(text="mark_notifications_as_read").pack())
keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[[button_mark_as_read]])


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("Привет", reply_markup=keyboard_reply)


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
    if notifications.totalCount == 0:
        await message.reply("Нет новых уведомлений!")
        return
    api_url_to_html_url = lambda u: "https://github.com" + u.removeprefix("https://api.github.com/repos")
    content = as_list(
        Bold("Уведомления:"),
        *[Text(TextLink(n.subject.title, url=api_url_to_html_url(n.subject.url)), f" - {updated_at_to_formatted_timedelta(n.updated_at)}")
          for n in notifications]
    )
    await message.reply(**content.as_kwargs(), reply_markup=keyboard_inline)


@dp.callback_query(PlainCallback.filter(F.text == "mark_notifications_as_read"))
async def callback_mark_notifications_as_read(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = await crud.user.get_user_by_user_id(user_id=user_id)
    if user is None:
        await call.answer("Сначала зарегестрируйтесь с помощью команды /login")
        return
    mark_notifications_as_read(access_token=user.gh_access_token)
    await call.answer("Все уведомления успешно очищены!")


async def main() -> None:
    bot = Bot(settings.bot_token)
    await init()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
