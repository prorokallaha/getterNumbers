from typing import Dict, Tuple


def test_button() -> Tuple[Dict[str, str], ...]:
    return (
        {'text': 'Inner Chat', 'callback_data': 'inner_chat_test'},
    )

def back_button() -> Dict[str, str]:
    return {'text': 'Back', 'callback_data': 'back'}


def next_pagination_button() -> Dict[str, str]:
    return {'text': 'Next', 'callback_data': 'next'}


def previous_pagination_button() -> Dict[str, str]:
    return {'text': 'Previous', 'callback_data': 'previous'}

