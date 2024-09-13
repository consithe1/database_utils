import json
import traceback


def decode_json(value: str | bytes | bytearray) -> tuple[bool, any]:
    """
    Function to convert bytes to a json/dict
    :param value: the item to decode
    :return: a tuple, the result of the decoding and the value decoded
    """
    is_json: bool = True
    decoded_value = value
    try:
        decoded_value = json.loads(value)
    except json.JSONDecodeError:
        is_json = False
    except UnicodeDecodeError:
        is_json = False

    return is_json, decoded_value
