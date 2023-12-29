#TODO мигрировать на 3.х

from datetime import datetime
from database.db_scripts import DbMethods
from database.connection_fabric import get_db_conn
from config_data.config import ADMIN
from middlware.middleware import MyMiddleWare
from tgset import my_disp

from handlers import admin_cmd, delete_admin, help, new_admin, send, start, status


async def on_startup(_):
    print("Бот успещно запущен")
    DbMethods.db_create(conn=get_db_conn())
    DbMethods.add_user(user_id=ADMIN,
                       admin=1,
                       donor_id=ADMIN,
                       active=1,
                       last_active=str(datetime.now()),
                       conn=get_db_conn())
    print("База данных подключена. Админ добавлен в базу данных.")


if __name__ == "__main__":
    # регистрируем middleware в диспетчере сразу для всех обновлений (событий)
    my_disp.update.outer_middleware.register(MyMiddleWare)
    executor.start_polling(dispatcher=my_disp,
                           skip_updates=True,
                           on_startup=on_startup)
