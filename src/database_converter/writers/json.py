import json


from database_converter.utils.utils import conversion_for_writing


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
                sanitized_row = {}
                for key, value in row.items():
                    sanitized_row[key] = conversion_for_writing(value)
                sanitized_table.append(sanitized_row)
            sanitized_db[table_name] = sanitized_table
        sanitized_content[db_name] = sanitized_db

    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(sanitized_content, indent=4))
