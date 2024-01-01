#TODO использовать шифрование данных secret_str

from aiogram import Bot
from config_data.config import API_KEY

my_bot = Bot(token=API_KEY, parse_mode="HTML")
