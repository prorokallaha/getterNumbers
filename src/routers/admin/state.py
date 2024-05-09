from aiogram.filters.state import State, StatesGroup


class CommandCreation(StatesGroup):
    waiting_for_tag = State()
    waiting_for_text = State()
    waiting_for_image = State()


class CommandRemove(StatesGroup):
    waiting_for_tag = State()