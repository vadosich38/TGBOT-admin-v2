from main import my_disp
from database.db_scripts import check_user_status
from aiogram.dispatcher import FSMContext
from states.states import MyStatesGroup
from aiogram import types


@my_disp.message_handler(commands=["delete_admin"])
async def delete_admin(message: types.Message):
    res = await check_user_status(user_id=message.from_user.id)
    if res == "admin":
        await message.answer(text="А теперь пришлите TELEGRAM ID пользователя, которого нужно исключить из списка"
                                  "администраторов")
        await MyStatesGroup.wait_id_to_delete.set()
    else:
        await message.reply(text="Вы не являетесь администратором для выполнения этого действия!")


@my_disp.message_handler(state=MyStatesGroup.wait_id_to_delete)
async def id_to_delete_admin(message: types.Message, state: FSMContext):
    res = len(message.text)
    if 9 <= res <= 10:
        await message.reply(text="ID указан корректно, ищу пользователя в БД...")
        res = await check_user_status(user_id=message.text)

        if res == "admin":
            await delete_admin()
        elif res == "not admin":
            await message.reply(text="Пользователь не является администратором")
            await state.finish()

    else:
        await message.reply(text="ID пользователя указан не верно! Длина ID составляет 9 или 10 символов."
                                 "\nПопробуйте снова или отменить добавление администратора /cancel_deleting")


@my_disp.message_handler(state=MyStatesGroup.wait_id_to_delete,
                         commands=["cancel_deleting"])
async def cancel_deleting(message: types.Message, state: FSMContext):
    await message.reply("Вы отменили удаление администратора")
    await state.finish()
