from aiogram.fsm.state import StatesGroup, State
#TODO документировать


class MyStatesGroup(StatesGroup):

    wait_id = State()
    wait_id_to_delete = State()
    send = State()
