from src.keyboards.default import get_default_button


def history_messages():
    return get_default_button(text="История сообщений", callback_data="history_messages")
