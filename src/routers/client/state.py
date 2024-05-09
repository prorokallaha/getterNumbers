from aiogram.filters.state import State, StatesGroup


class CodeRequest(StatesGroup):
    get_number = State()
    waiting_for_code = State()
    aproove_noaprove = State()
