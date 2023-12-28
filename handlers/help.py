from aiogram import types
from main import my_disp
from config_data.config import HELP_TEXT


@my_disp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.reply(text=HELP_TEXT)
