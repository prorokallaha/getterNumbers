from typing import Dict

from src.keyboards.button import button


def aproove() -> Dict[str, str]:
    return button(text="✅", callback_data="aproove")


def not_aproove() -> Dict[str, str]:
    return button(text="❌", callback_data="not_aproove")
