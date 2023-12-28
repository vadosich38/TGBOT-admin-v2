from aiogram.dispatcher.filters.state import StatesGroup, State


class MyStatesGroup(StatesGroup):

    wait_id = State()
    wait_id_to_delete = State()
    send = State()
