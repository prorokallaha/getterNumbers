from src.keyboards.default import get_default_button


def select_users():
    return get_default_button(text="Показать пользователей", callback_data="select_users")
