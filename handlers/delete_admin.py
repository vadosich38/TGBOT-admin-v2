from database import DbMethods
from database.connection_fabric import get_db_conn
from states.states import MyStatesGroup

from aiogram import types
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

delete_admin_router = Router()


@delete_admin_router.message(Command("delete_admin"))
async def delete_admin(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер команды /delete_admin
    вызывает процесс разжалования администратора до обычного пользователя
    если вызвавший команду пользователь является админом бота, состояние бота меняется на wait_id_to_delete
    :param message: объект сообщения
    :param state: объект состояния бота
    :return: None
    """
    res = DbMethods.check_user_status(user_id=message.from_user.id, conn=get_db_conn())
    if res == "admin":
        await message.answer(text="А теперь пришлите TELEGRAM ID пользователя, которого нужно исключить из списка"
                                  "администраторов")
        await state.set_state(MyStatesGroup.wait_id_to_delete)
    else:
        await message.reply(text="Вы не являетесь администратором для выполнения этого действия!")


@delete_admin_router.message(StateFilter(MyStatesGroup.wait_id_to_delete))
async def id_to_delete_admin(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер сообщения, принимает TELEGRAM ID пользователя, которого нужно разжаловать
    срабатывает только в состоянии бота wait_id_to_delete
    после успешного разжалования состояние бота очищается
    иначе состояние сохраняется до ввода корректного ID или команды /cancel
    :param message: объект сообщения
    :param state: объект состояния бота
    :return: None
    """
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
async def cancel_deleting_cmd(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер команды /cancel
    вызывает отмену удаления бота
    очищает состояние бота
    срабатывает только в состоянии бота wait_id_to_delete
    :param message: объект сообщения
    :param state: объект состояния бота
    :return: None
    """
    await message.reply("Вы отменили удаление администратора")
    await state.clear()
