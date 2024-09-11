import blackboxprotobuf as bk
from func_timeout import func_timeout, FunctionTimedOut
import traceback

import database_converter.utils.constants as constants
from database_converter.utils.logger import logger
from database_converter.utils.utils import control_chars_bytes


def decode_protobuf(value: bytes) -> tuple[bool, any]:
    """
    Function to interpret bytes as a protobuf if possible.
    :param value: bytes to decode
    :return: a tuple with a boolean representing if the conversion worked or not, and the value converted if it was a
    success else return the value given as a parameter
    """
    is_protobuf: bool = True
    try:
        logger.debug('Trying to convert bytes to protobuf and decoding it')
        decoded_protobuf = \
            func_timeout(timeout=10, func=bk.decode_message, kwargs={'buf': value})[0]
        value = decode_protobuf_content(decoded_protobuf)
    except FunctionTimedOut as e:
        traceback.print_exception(e)
        is_protobuf = False
    except Exception as e:
        traceback.print_exception(e)
        is_protobuf = False

    return is_protobuf, value


def decode_protobuf_content(protobuf: dict[str, any]) -> dict[str, any]:
    """
    Decode recursively a nested dict. Try to decode bytes array, etc.
    :param protobuf: a dictionary
    :return: a decoded dictionary
    """
    for key, value in protobuf.items():
        if isinstance(value, dict):
            protobuf[key] = "Chat" if value == constants.CHAT_EQUIVALENT else decode_protobuf_content(value)
        elif isinstance(value, bytes):
            if not any(byte in value for byte in control_chars_bytes):
                try:
                    protobuf[key] = value.decode("utf-8").replace('\t', '').replace('\n', '')
                except UnicodeDecodeError as e:
                    # error occurred while decoding in utf-8
                    traceback.print_exception(e)
                    protobuf[key] = value
        elif isinstance(value, list):
            for i in range(len(value)):
                protobuf[key][i] = decode_protobuf_content(value[i]) if isinstance(value[i], dict) else value[i]
        elif isinstance(value, int) or isinstance(value, float):
            protobuf[key] = value
        elif isinstance(value, str):
            protobuf[key] = value.replace('\t', '').replace('\n', '')

    return protobuf
