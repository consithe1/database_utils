import sqlite3

from database_converter.utils.utils import dict_factory, convert_multidimensional_to_single_dimensional
from database_converter.decoders.json import decode_json
from database_converter.decoders.protobuf import decode_protobuf
from database_converter.utils.logger import logger_error


def process_row(row: dict[str, any]) -> dict[str, any]:
    """
    Function to process a row (i.e. interpreting bytes as json dictionaries or protobuf) and convert a nested dictionary
    to a simple one
    :param row: a python dictionary
    :return: a python dictionary
    """
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
    """
    Function to process the rows of a database table.
    :param rows: a list of python dictionaries
    :return: a list of python dictionaries
    """

    return [process_row(row) for row in rows]


class DatabaseFileConverter:
    """
    Class to convert a database file and its content to a python dictionary.

    This class should NOT be instantiated directly.
    """
    def __init__(self, filepath: str, n_threads: int):
        """
        Function to instantiate a database converter
        :param filepath: the path to a database file
        :param n_threads: the max number of threads to use
        """
        self.db_file: str = filepath
        self.n_threads: int = n_threads

    def extract_rows(self, table_name) -> dict[str, any]:
        """
        Function to extract rows from a database table.
        :param table_name: the name of the table to extract rows from
        :return: a python dictionary representing the table and its content
        """
        table_decoded_rows = []
        with sqlite3.connect(self.db_file) as conn:
            # get the results of statements as a python dictionary
            conn.row_factory = dict_factory
            # get all the rows from the table
            rows_from_table = conn.execute(f'SELECT * FROM {table_name}')
            all_rows = []
            try:
                all_rows = rows_from_table.fetchall()
            except sqlite3.OperationalError as e:
                logger_error.error(f'Failed to get the rows from {table_name}: {e}')

            # process rows
            if all_rows:
                table_decoded_rows = process_rows(all_rows)

        decoded_table = {
            table_name: table_decoded_rows
        }

        return decoded_table
