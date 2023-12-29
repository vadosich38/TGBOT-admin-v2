from aiogram import types
from config_data.config import ADMIN_TEXT
from aiogram import Router
from aiogram.filters import Command
#TODO документировать

admin_cmd_router = Router()


@admin_cmd_router.message(Command("admin"))
async def admin_cmd(message: types.Message):
    await message.answer(text=ADMIN_TEXT)
