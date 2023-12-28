from aiogram import types
from main import my_disp
from database.db_scripts import check_user_status


@my_disp.message_handler(commands=["status"])
async def cmd_status(message: types.Message):
    status = await check_user_status(user_id=message.from_user.id)
    await message.answer(text="Ваш статус: {}".format(status))
