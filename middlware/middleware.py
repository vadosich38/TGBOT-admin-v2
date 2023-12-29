from typing import Any, Awaitable, Callable, Dict, Union

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.dispatcher.middlewares.error import CancelHandler
#TODO документировать


class MyMiddleWare(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        print("\nОтправлено сообщение в чате типа:", event.chat.type)
        if event.chat.type != "private":
            print("Сообщение или команда не будет обработаны, так как вызваны не в личном чате!")
            raise CancelHandler
        return await handler(event, data)
