from aiogram.fsm.state import StatesGroup, State


class MyStatesGroup(StatesGroup):
    """
    Класс машины состояний бота

    wait_id - ожидание TELEGRAM ID пользователя для добавления нового пользователя
    wait_id_to_delete - ожидание TELEGRAM ID пользователя для разжалования админа
    send - состояние рассылки
    """
    wait_id = State()
    wait_id_to_delete = State()
    send = State()
