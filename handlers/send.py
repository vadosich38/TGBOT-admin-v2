from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.exceptions import TelegramAPIError
from datetime import datetime
from aiogram.filters import Command, StateFilter
from aiogram import Router

from states.states import MyStatesGroup
from database.db_scripts import DbMethods
from tgset import my_bot
from database.connection_fabric import get_db_conn

send_cmd_router = Router()


@send_cmd_router.message(Command("send"))
async def send_cmd(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер команды /send
    если команду вызвал администратор, он получает приглашения прислать текст рассылки. Состояние бота меняется на send
    Иначе, сообщение об ошибке
    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    res = DbMethods.check_user_status(user_id=message.from_user.id, conn=get_db_conn())
    if res == "admin":
        await message.reply("Теперь пришлите сообщение, которое нужно разослать пользователям бота."
                            "\nЕсли вы хотите отменить рассылку, пришлите команду /cancel")
        await state.set_state(MyStatesGroup.send)
    else:
        await message.reply("Вы не администратор, рассылку включает только администратор!")


@send_cmd_router.message(StateFilter(MyStatesGroup.send))
async def new_text_send(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер сообщения, принимающий текст для рассылки. Срабатывает только в состоянии бота send
    после записи текста в память состояния бота, пользователю предлагается подтвердить правильность текста
    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await message.answer(text="Ваше сообщение будет выглядеть так:")
    await my_bot.send_message(chat_id=message.from_user.id,
                              text=message.text)

    await state.update_data(ads_text=message.text)
    await message.answer(text="Если вы хотите изменить текст, отправьте его снова. Если текст вас устраивает,"
                              "отправьте команду /confirm")


@send_cmd_router.message(StateFilter(MyStatesGroup.send), Command("confirm"))
async def confirm_cmd(state: FSMContext) -> None:
    """
    Колбек хендлер подтверждения корректности текста рассылки
    срабатывает только в состоянии бота send
    выполняется рассылка текста, после окончания рассылки состояние текста очищается
    :param state: объект состояния
    :return: None
    """
    users_list = DbMethods.get_users_id(conn=get_db_conn())

    success = 0
    failed = 0
    ads_data = await state.get_data()

    for user_id in users_list:
        try:
            await my_bot.send_message(chat_id=user_id[0],
                                      text=ads_data["send_text"])
            DbMethods.update_user_data(user_id=user_id[0], active=1, last_active=str(datetime.now()), conn=get_db_conn())
            success += 1
        except TelegramAPIError as ex:
            DbMethods.update_user_data(user_id=user_id[0], active=0, conn=get_db_conn())
            print("Сообщение не отправлено:", ex)
            failed += 1
    else:
        print("Рассылка звершена. Успешно отправлено {} сообщений, {} сообщений не было доставлено".format(
            success, failed))

    await state.clear()


@send_cmd_router.message(Command("cancel"), StateFilter(MyStatesGroup.send))
async def cancel_send_cmd(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер команды /cancel
    команда отменяет рассылку текста
    состояние бота очищается
    :param message: объект сообщения
    :param state: объект состояния
    :return: None
    """
    await message.reply("Вы отменили создание рассылки")
    await state.clear()
