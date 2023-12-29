from database import DbMethods
from database.connection_fabric import get_db_conn
from states.states import MyStatesGroup

from aiogram import types
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
#TODO документировать

delete_admin_router = Router()


@delete_admin_router.message(Command("delete_admin"))
async def delete_admin(message: types.Message, state: FSMContext):
    res = DbMethods.check_user_status(user_id=message.from_user.id, conn=get_db_conn())
    if res == "admin":
        await message.answer(text="А теперь пришлите TELEGRAM ID пользователя, которого нужно исключить из списка"
                                  "администраторов")
        await state.set_state(MyStatesGroup.wait_id_to_delete)
    else:
        await message.reply(text="Вы не являетесь администратором для выполнения этого действия!")


@delete_admin_router.message(StateFilter(MyStatesGroup.wait_id_to_delete))
async def id_to_delete_admin(message: types.Message, state: FSMContext):
    if 9 <= len(message.text.strip()) <= 10:
        await message.reply(text="ID указан корректно, ищу пользователя в БД...")
        res = DbMethods.check_user_status(user_id=int(message.text.strip()), conn=get_db_conn())

        if res == "admin":
            DbMethods.delete_admin(user_id=int(message.text.strip()), conn=get_db_conn())
        elif res == "not admin":
            await message.reply(text="Пользователь не является администратором")
            await state.clear()

    else:
        await message.reply(text="ID пользователя указан не верно! Длина ID составляет 9 или 10 символов."
                                 "\nПопробуйте снова или отменить добавление администратора /cancel_deleting")


@delete_admin_router.message(StateFilter(MyStatesGroup.wait_id_to_delete),
                             Command("cancel_deleting"))
async def cancel_deleting_cmd(message: types.Message, state: FSMContext):
    await message.reply("Вы отменили удаление администратора")
    await state.clear()
