from datetime import datetime
from aiogram import types
from database.db_scripts import DbMethods
from config_data.config import START_TEXT
from aiogram import Router
from aiogram.filters import CommandStart

start_router = Router()


@start_router.message(CommandStart)
async def start_cmd(message: types.Message):
    await message.delete()
    DbMethods.add_user(user_id=message.from_user.id,
                       admin=0,
                       donor_id=0,
                       active=1,
                       last_active=str(datetime.now()))
    await message.answer(text=START_TEXT)
