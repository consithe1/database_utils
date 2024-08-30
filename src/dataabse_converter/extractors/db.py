import sqlite3

from dataabse_converter.utils.utils import dict_factory, convert_multidimensional_to_single_dimensional
from dataabse_converter.decoders.json import decode_json
from dataabse_converter.decoders.protobuf import decode_protobuf


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
