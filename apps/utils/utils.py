from typing import Any
import json


def force_string(value: Any) -> str:
    '''
    Force a value to be a string.
    '''
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, dict):
        return json.dumps(value)
    elif value is None:
        return ''
    else:
        return str(value)
