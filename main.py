from aiogram import Bot
from datetime import datetime
import asyncio

from database.db_scripts import DbMethods
from database.connection_fabric import get_db_conn
from config_data.config import ADMIN
from middlware.middleware import MyMiddleWare
from tgset.bot_set import my_bot
from tgset.dispatcher_set import my_disp

from handlers.start import start_router
from handlers.start import start_cmd

from handlers.help import help_cmd_router
from handlers.help import help_cmd

from handlers.status import status_cmd_router
from handlers.status import status_cmd

from handlers.admin_cmd import admin_cmd_router
from handlers.admin_cmd import admin_cmd

from handlers.delete_admin import delete_admin_router
from handlers.delete_admin import delete_admin, id_to_delete_admin, cancel_deleting_cmd

from handlers.new_admin import new_admin_router
from handlers.new_admin import new_admin_cmd, new_admin_id, cancel_cmd

from handlers.send import send_cmd_router
from handlers.send import send_cmd, new_text_send, cancel_send_cmd


def on_startup(bot: Bot):
    print("Бот успещно запущен")
    DbMethods.db_create(conn=get_db_conn())
    DbMethods.add_user(user_id=ADMIN,
                       admin=1,
                       donor_id=ADMIN,
                       active=1,
                       last_active=str(datetime.now()),
                       conn=get_db_conn())
    print("База данных подключена. Админ добавлен в базу данных.")


async def main() -> None:
    my_disp.startup.register(on_startup)
    my_disp.include_routers(start_router, help_cmd_router, admin_cmd_router, delete_admin_router, new_admin_router,
                            send_cmd_router, status_cmd_router)
    # регистрируем middleware в диспетчере сразу для всех обновлений (событий)
    my_disp.update.outer_middleware.register(MyMiddleWare())

    async with my_bot.context():
        await my_bot.delete_webhook(drop_pending_updates=True)
        try:
            await my_disp.start_polling(my_bot)
        except Exception as polling_error_obj:
            print("При полинге бота возникла ошибка!!!", polling_error_obj)
        finally:
            db_conn = get_db_conn()
            db_conn.commit()
            db_conn.close()


if __name__ == "__main__":
    asyncio.run(main())
