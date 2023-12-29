#TODO мигрировать на 3.х


from aiogram import Dispatcher
from .bot_set import my_bot
from middlware.middleware import MyMiddleWare

my_disp = Dispatcher(bot=my_bot)
