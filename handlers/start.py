from datetime import datetime
from aiogram import types
from database.db_scripts import add_user
from config_data.config import START_TEXT
from main import my_disp


@my_disp.message_handler(commands=["start"],
                         state="*")
async def cmd_start(message: types.Message):
    await message.delete()
    await add_user(user_id=message.from_user.id,
                   admin=0,
                   donor_id=0,
                   active=1,
                   last_active=str(datetime.now()))
    await message.answer(text=START_TEXT)
