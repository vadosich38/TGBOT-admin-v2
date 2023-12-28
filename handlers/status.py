from aiogram import types
from database.db_scripts import DbMethods
from aiogram import Router
from aiogram.filters import Command

status_cmd_router = Router()


@status_cmd_router.message(Command("status"))
async def status_cmd(message: types.Message):
    status = DbMethods.check_user_status(user_id=message.from_user.id)
    await message.answer(text="Ваш статус: {}".format(status))
