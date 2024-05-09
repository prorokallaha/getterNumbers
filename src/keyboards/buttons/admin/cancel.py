from src.keyboards.default import get_default_button


def cancel_button():
    return get_default_button(text='Отмена', callback_data="cancel")

