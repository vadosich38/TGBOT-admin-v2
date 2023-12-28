from aiogram.dispatcher import FSMContext
from aiogram import types
from states.states import MyStatesGroup
from database.db_scripts import update_user_data, get_users_id
from tgset import my_disp, my_bot
from aiogram.utils.exceptions import BotBlocked
from datetime import datetime


@my_disp.message_handler(commands=["cancel"],
                         state=MyStatesGroup.send)
async def cmd_cancel_send(message: types.Message, state: FSMContext):
    await message.reply("Вы отменили создание рассылки")
    await state.finish()


@my_disp.message_handler(state=MyStatesGroup.send,
                         commands=["confirm"])
async def cmd_confirm(state: FSMContext):
    users_list = await get_users_id()
    async with state.proxy() as data:
        data["succes"] = 0
        data["failed"] = 0
        for user_id in users_list:
            try:
                await my_bot.send_message(chat_id=user_id[0],
                                          text=data["send_text"])
                await update_user_data(user_id=user_id[0], active=1, last_active=str(datetime.now()))
                data["succes"] += 1
            except BotBlocked as ex:
                await update_user_data(user_id=user_id[0], active=0)
                print("Сообщение не отправлено:", ex)
                data["failed"] += 1
                # return True
        else:
            print("Рассылка звершена. Успешно отправлено {} сообщений, {} сообщений не было доставлено".format(
                data["succes"], data["failed"]))

    await state.finish()


@my_disp.message_handler(state=MyStatesGroup.send)
async def new_text_send(message: types.Message, state: FSMContext):
    await message.answer(text="Ваше сообщение будет выглядеть так:")
    await my_bot.send_message(chat_id=message.from_user.id,
                              text=message.text)

    async with state.proxy() as data:
        data["send_text"] = message.text

    await message.answer(text="Если вы хотите изменить текст, отправьте его снова. Если текст вас устраивает,"
                              "отправьте команду /confirm")
