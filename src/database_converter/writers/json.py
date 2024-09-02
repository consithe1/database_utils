import json


def create_json_from_row(row: dict[str, any]) -> dict[str, any]:
    """
    Function to create the json structure for a row
    :param row: a python dictionary
    :return: a python dictionary with the json structure
    """
    struct = {}

    for key, value in row.items():
        type_val = type(value).__name__
        if isinstance(value, bytes):
            value = value.hex()
        struct[key] = {'value': value, 'type': type_val}

    return struct


def write(dest_file: str, content: dict[str, any]):
    """
    Function to write a python dictionary as a json file.
    :param dest_file: the destination file
    :param content: a python dictionary
    :return:
    """
    sanitized_content = {}

    for db_name, db in content.items():
        sanitized_db = {}
        for table_name, table in db.items():
            sanitized_table = []
            for row in table:
                sanitized_row = create_json_from_row(row)
                sanitized_table.append(sanitized_row)

            sanitized_db[table_name] = sanitized_table
        sanitized_content[db_name] = sanitized_db

    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(sanitized_content, indent=4))
