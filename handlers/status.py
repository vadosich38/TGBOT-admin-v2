from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from database.db_scripts import DbMethods
from database.connection_fabric import get_db_conn

status_cmd_router = Router()


@status_cmd_router.message(Command("status"))
async def status_cmd(message: types.Message) -> None:
    """
    Хендлер команды /status
    возвращает актуальный статус пользователя в БД
    :param message: объект сообщения
    :return: None
    """
    status = DbMethods.check_user_status(user_id=message.from_user.id, conn=get_db_conn())
    await message.answer(text="Ваш статус: {}".format(status))
