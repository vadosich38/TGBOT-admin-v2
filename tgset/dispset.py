from aiogram import Dispatcher
from .botset import my_bot
from .storageset import my_storage

my_disp = Dispatcher(bot=my_bot,
                     storage=my_storage)
