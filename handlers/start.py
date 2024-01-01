from datetime import datetime
from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart

from database.db_scripts import DbMethods
from config_data.config import START_TEXT
from database.connection_fabric import get_db_conn

start_router = Router()


@start_router.message(CommandStart)
async def start_cmd(message: types.Message) -> None:
    """
    Хендлер команды /start
    добавдяет в БД нового пользователя и присылает приветственное сообщение
    :param message: объект сообщения
    :return: None
    """
    await message.delete()
    DbMethods.add_user(user_id=message.from_user.id,
                       admin=0,
                       active=1,
                       last_active=str(datetime.now()), conn=get_db_conn())
    await message.answer(text=START_TEXT)
