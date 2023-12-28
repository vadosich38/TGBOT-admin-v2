from main import my_disp
from aiogram import types
from database.db_scripts import check_user_status, update_to_admin
from states.states import MyStatesGroup
from aiogram.dispatcher import FSMContext


@my_disp.message_handler(commands=["new_admin"])
async def cmd_new_admin(message: types.Message):
    res = await check_user_status(user_id=message.from_user.id)
    if res == "admin":
        await MyStatesGroup.wait_id.set()
        await message.answer(text="Теперь пришлите мне TELEGRAM ID пользователя, который будет администратором")
    else:
        await message.reply(text="Вы не являетесь администратором чтобы добавить другого администратора.\n"
                                 "Как стать администратором - /admin")


@my_disp.message_handler(commands=["cancel"],
                         state=MyStatesGroup.wait_id)
async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.reply(text="Вы отменили добавление нового администратора!")
    await state.finish()


@my_disp.message_handler(state=MyStatesGroup.wait_id)
async def new_admin_id(message: types.Message, state: FSMContext):
    if 9 <= len(message.text) <= 10:
        await message.reply(text="ID указан корректно, ищу пользователя в БД...")
        status = await check_user_status(message.text)
        if status == "no user":
            await message.answer(text="Такой пользователь не найден. Сначала пользователь должен запустить бота."
                                      "\nПопробуйте снова или отмените добавление администратора /cancel")
        elif status == "admin":
            await message.answer("Пользователь найден")
            await message.answer(text="Пользователь уже является администратором!")
            await state.finish()
        elif status == "not admin":
            await message.answer("Пользователь найден")
            await update_to_admin(user_id=message.text,
                                  donor_id=message.from_user.id)
            await message.answer("Пользователь успешно назначен администратором!")
            await state.finish()

    else:
        await message.reply(text="ID пользователя указан не верно! Длина ID составляет 9 или 10 символов."
                                 "\nПопробуйте снова или отменить добавление администратора /cancel")


@my_disp.message_handler(commands=["send"])
async def cmd_send(message: types.Message):
    res = await check_user_status(user_id=message.from_user.id)
    if res == "admin":
        await message.reply("Теперь пришлите сообщение, которое нужно разослать пользователям бота."
                            "\nЕсли вы хотите отменить рассылку, пришлите команду /cancel")
        await MyStatesGroup.send.set()
    else:
        await message.reply("Вы не администратор, рассылку включает только администратор!")
