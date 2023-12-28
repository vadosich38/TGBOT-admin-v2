from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler


class MyMiddleWares(BaseMiddleware):
    @classmethod
    async def on_process_message(cls, message: types.Message, data: dict):
        print("\nОтправлено сообщение в чате типа:", message.chat.type)
        if message.chat.type != "private":
            print("Сообщение или команда не будет обработаны, так как вызваны не в личном чате!")
            raise CancelHandler


