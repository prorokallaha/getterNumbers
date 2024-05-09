from src.keyboards.default import get_default_button


def add_commands():
    return get_default_button(text='Сделать команду', callback_data="create_command")


def update_commands():
    return get_default_button(text="Изменить команду", callback_data="update_command")


def delete_commands():
    return get_default_button(text="Удалить команду", collback_data="delete_command")
