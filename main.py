from aiogram import executor
from datetime import datetime
from database.db_scripts import db_create, add_user
from config_data.config import ADMIN
from middlware.middleware import MyMiddleWares
from tgset import my_disp

from handlers import admin, delete_admin, help, new_admin, send, start, status


async def on_startup(_):
    print("Бот успещно запущен")
    await db_create()
    await add_user(user_id=ADMIN,
                   admin=1,
                   donor_id=ADMIN,
                   active=1,
                   last_active=str(datetime.now()))
    print("База данных подключена. Админ добавлен в базу данных.")


if __name__ == "__main__":
    my_disp.setup_middleware(middleware=MyMiddleWares())
    executor.start_polling(dispatcher=my_disp,
                           skip_updates=True,
                           on_startup=on_startup)
