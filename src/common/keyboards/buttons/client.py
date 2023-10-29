from typing import Dict, Tuple

from src.common.middlewares.i18n import gettext as _


def test_button() -> Tuple[Dict[str, str], ...]:
    '''
    We can transalate our inline button as well, it'll we traslated right it is called
    '''
    return (
        {'text': _('test'), 'callback_data': 'test'},
        {'text': _('Inner Chat'), 'callback_data': 'inner_chat_test'},
    )


def back_button() -> Dict[str, str]:
    return {'text': _('Back'), 'callback_data': 'back'}


def next_pagination_button() -> Dict[str, str]:
    return {'text': _('Next'), 'callback_data': 'next'}


def previous_pagination_button() -> Dict[str, str]:
    return {'text': _('Previous'), 'callback_data': 'previous'}


def pagination_data_button(data: Tuple[str, str]) -> Dict[str, str]:
    text, cbdata = data
    return {'text': text, 'callback_data': f'data:{cbdata}'}