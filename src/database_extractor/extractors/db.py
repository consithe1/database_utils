import sqlite3
import json
from func_timeout import func_timeout, FunctionTimedOut
import blackboxprotobuf as bk


from database_extractor.utils.utils import dict_factory, convert_multidimensional_to_single_dimensional
from database_extractor.utils.logger import logger, logger_error
import database_extractor.utils.constants as constants


def decode_protobuf(value: bytes) -> tuple[bool, any]:
    is_protobuf: bool = True
    try:
        logger.debug('Trying to convert bytes to protobuf and decoding it')
        decoded_protobuf = \
            func_timeout(timeout=10, func=bk.decode_message, kwargs={'buf': value})[0]
        value = decode_protobuf_content(decoded_protobuf)
    except FunctionTimedOut:
        logger_error.error("Protobuf decoding timed out")
        is_protobuf = False
    except Exception as e:
        logger_error.error(f'Failed to decode protobuf because of this error: {e}')
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
            if value == constants.CHAT_EQUIVALENT:
                protobuf[key] = "Chat"
            else:
                protobuf[key] = decode_protobuf_content(value)
        elif isinstance(value, bytes):
            try:
                protobuf[key] = value.decode("utf-8").replace('\t', '').replace('\n', '')
            except UnicodeDecodeError:
                # error occurred while decoding in utf-8
                logger.debug('Failed to convert bytes to string')
                protobuf[key] = value
        elif isinstance(value, list):
            for i in range(len(value)):
                protobuf[key][i] = decode_protobuf_content(value[i]) if isinstance(value[i], dict) else value[
                    i]
        elif isinstance(value, int) or isinstance(value, float):
            protobuf[key] = value
        elif isinstance(value, str):
            protobuf[key] = value.replace('\t', '').replace('\n', '')

    return protobuf


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


def process_row(row: dict[str, any]) -> dict[str, any]:
    decoded_row: dict = {}

    for key, value in row.items():
        tmp_val = value
        if isinstance(tmp_val, bytes):
            # decode json
            is_json, tmp_val = decode_json(tmp_val)
            # decode protobuf
            if not is_json:
                is_protobuf, tmp_val = decode_protobuf(tmp_val)

        decoded_row[key] = tmp_val

    decoded_row = convert_multidimensional_to_single_dimensional(decoded_row)

    return decoded_row


def process_rows(rows: list[dict[str, any]]) -> list[dict[str, any]]:
    decoded_rows: list[dict[str, any]] = []

    for row in rows:
        decoded_rows.append(process_row(row))

    return decoded_rows


class DatabaseFileExtractor:
    def __init__(self, filepath: str, n_threads: int = 8):
        self.db_file: str = filepath
        self.n_threads: int = n_threads

    def extract_rows(self, table_name):
        table_decoded_rows = []
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = dict_factory

            rows_from_table = conn.execute(f'SELECT * FROM {table_name}')

            all_rows = []
            try:
                all_rows = rows_from_table.fetchall()
            except sqlite3.OperationalError as e:
                pass

            # process rows
            if all_rows:
                table_decoded_rows = process_rows(all_rows)

        decoded_table = {
            table_name: table_decoded_rows
        }

        return decoded_table
