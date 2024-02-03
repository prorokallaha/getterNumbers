from typing import (
    Any,
    Callable,
    Dict,
    Final,
    List,
    Mapping,
    Sequence,
    TypeGuard,
    Union,
)

from aiogram import types

from src.keyboards.inline import get_inline_button, inline_keyboard

DEFAULT_STEP: Final[int] = 2


def is_list_or_tuple_of_type(
    _type: Any,
    data: Sequence[Union[Dict[str, Any], str]],
) -> TypeGuard[Sequence[Union[Dict[str, Any], str]]]:
    if not isinstance(data, (list, tuple)):
        raise TypeError(f"data should be list or tuple type, not {type(data)}")
    is_all_true = [isinstance(value, _type) for value in data]
    return all(is_all_true)


def build_buttons(
    buttons: List[Union[types.KeyboardButton, types.InlineKeyboardButton]],
    sep: int = DEFAULT_STEP,
) -> List[List[Union[types.KeyboardButton, types.InlineKeyboardButton]]]:
    return [buttons[n : n + sep] for n in range(0, len(buttons), sep)]


def build_markup(
    data: Union[Sequence[Union[Dict[str, Any], str]], Mapping[str, Any]],
    keyboard: Callable[
        ..., Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup]
    ] = inline_keyboard,
    buttons: Callable[
        ..., Union[types.KeyboardButton, types.InlineKeyboardButton]
    ] = get_inline_button,
    sep: int = DEFAULT_STEP,
) -> Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup]:
    if not callable(keyboard) and not callable(buttons):
        raise TypeError("keyboard and buttons params should be callable function")

    if isinstance(data, dict):
        return keyboard([[buttons(**data)]])
    elif isinstance(data, str):
        return keyboard([[buttons(text=data)]])
    elif isinstance(data, (tuple, list)):
        if is_list_or_tuple_of_type(dict, data):
            return keyboard(build_buttons([buttons(**value) for value in data], sep))
        if is_list_or_tuple_of_type(str, data):
            return keyboard(build_buttons([buttons(text=value) for value in data], sep))

    raise TypeError(f"Got unexpected type {type(data)}")
