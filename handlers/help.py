from aiogram import types
from config_data.config import HELP_TEXT
from aiogram.filters import Command
from aiogram import Router

help_cmd_router = Router()


@help_cmd_router.message(Command("help"))
async def help_cmd(message: types.Message) -> None:
    """
    Хендлер команды /help
    возвращает сообщение с инструкцией, какие команды выполняет бот
    :param message: объект сообщения
    :return: None
    """
    await message.reply(text=HELP_TEXT)
