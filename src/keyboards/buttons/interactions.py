from typing import Dict

from src.keyboards.button import button


def back_button() -> Dict[str, str]:
    return button(text="Back", callback_data="back")


def next_pagination_button() -> Dict[str, str]:
    return button(text="Next", callback_data="next")


def previous_pagination_button() -> Dict[str, str]:
    return button(text="Previous", callback_data="previous")
