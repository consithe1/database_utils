import json


def load_dict_from_json(json_obj):
    decoded_json = {}
    for db_name, db in json_obj.items():
        decoded_db = {}
        for table_name, table in db.items():
            decoded_table = []
            for row in table:
                decoded_row = {}

                for col_key, col_value in row.items():
                    val = col_value.get('value')
                    typ = col_value.get('type')

                    if typ == 'int':
                        val = int(val)
                    elif typ == 'float':
                        val = float(val)
                    elif typ == 'NoneType':
                        val = None
                    elif typ == 'bytes':
                        val = bytes.fromhex(val)

                    decoded_row[col_key] = val

                decoded_table.append(decoded_row)
            decoded_db[table_name] = decoded_table

        decoded_json[db_name] = decoded_db

    return decoded_json


def read(source_file: str) -> dict[str, any]:
    with open(source_file, 'r') as f:
        data = json.load(f)
        decoded_data = load_dict_from_json(data)

    return decoded_data
