import xml.etree.ElementTree as ET


from database_converter.utils.utils import conversion_from_reading


def read(source_file: str) -> dict[str, any]:
    """
    Function to read a specific XML formated file and cast it into a dictionary python object
    :param source_file: XML formated file
    :return: dictionary python object
    """
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(source_file, parser)

    db = tree.getroot()
    db_name: str = db.get("name")

    db_dict: dict[str, any] = {}
    for table in db.findall("table"):
        table_name: str = table.get("name")

        table_rows: list = []
        for row in table.findall("row"):
            row_dict: dict[str, any] = {}
            for col in row.findall("column"):
                col_key = col.get("key")
                col_type = col.get("type")
                col_val = col.get("value")

                row_dict[col_key] = conversion_from_reading(col_val, col_type)

            table_rows.append(row_dict)
        # add the table read to the database dictionary
        db_dict[table_name] = table_rows

    return {db_name: db_dict}
