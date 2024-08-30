import json


def decode_json(value: bytes) -> tuple[bool, any]:
    """
    Function to convert bytes to a json/dict
    :param value: the item to decode
    :return: a tuple, the result of the decoding and the value decoded
    """
    is_json: bool = True
    try:
        value = json.loads(value.decode('utf-8'))
    except json.JSONDecodeError:
        is_json = False
    except UnicodeDecodeError:
        is_json = False

    return is_json, value
