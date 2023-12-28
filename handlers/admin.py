from aiogram import types
from main import my_disp
from config_data.config import ADMIN_TEXT


@my_disp.message_handler(commands=["admin"])
async def cmd_admin(message: types.Message):
    await message.answer(text=ADMIN_TEXT)
