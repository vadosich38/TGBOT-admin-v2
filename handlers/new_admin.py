from database.db_scripts import DbMethods
from database.connection_fabric import get_db_conn
from states.states import MyStatesGroup

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.filters import Command, StateFilter
#TODO документировать

new_admin_router = Router()


@new_admin_router.message(Command("new_admin"))
async def new_admin_cmd(message: types.Message, state: FSMContext):
    res = DbMethods.check_user_status(user_id=message.from_user.id, conn=get_db_conn())
    if res == "admin":
        await state.set_state(MyStatesGroup.wait_id)
        await message.answer(text="Теперь пришлите мне TELEGRAM ID пользователя, который будет администратором")
    else:
        await message.reply(text="Вы не являетесь администратором чтобы добавить другого администратора.\n"
                                 "Как стать администратором - /admin")


@new_admin_router.message(StateFilter(MyStatesGroup.wait_id))
async def new_admin_id(message: types.Message, state: FSMContext):
    if 9 <= len(message.text.strip()) <= 10:
        await message.reply(text="ID указан корректно, ищу пользователя в БД...")
        status = DbMethods.check_user_status(user_id=int(message.text.strip()), conn=get_db_conn())
        if status == "no user":
            await message.answer(text="Такой пользователь не найден. Сначала пользователь должен запустить бота."
                                      "\nПопробуйте снова или отмените добавление администратора /cancel")
        elif status == "admin":
            await message.answer("Пользователь найден")
            await message.answer(text="Пользователь уже является администратором!")
            await state.clear()
        elif status == "not admin":
            await message.answer("Пользователь найден")
            DbMethods.update_to_admin(user_id=int(message.text.strip()),
                                      donor_id=message.from_user.id)
            await message.answer("Пользователь успешно назначен администратором!")
            await state.clear()

    else:
        await message.reply(text="ID пользователя указан не верно! Длина ID составляет 9 или 10 символов."
                                 "\nПопробуйте снова или отменить добавление администратора /cancel")


@new_admin_router.message(Command("cancel"), StateFilter(MyStatesGroup.wait_id))
async def cancel_cmd(message: types.Message, state: FSMContext):
    await message.reply(text="Вы отменили добавление нового администратора!")
    await state.clear()
