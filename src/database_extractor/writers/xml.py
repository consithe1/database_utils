import xml.etree.ElementTree as ET


from database_extractor.utils.utils import remove_control_chars


def write(dest_file: str, content: dict[str, any]):
    root = ET.Element('database')

    if len(content.keys()) != 1:
        pass
    else:
        db_name = str(list(content.keys())[0])
        root.set('name', db_name)

        for table_name, table in content.get(db_name).items():
            table_xml = ET.SubElement(root, 'table')
            table_xml.set("name", table_name)

            for row in table:
                row_xml = ET.SubElement(table_xml, 'row')
                for key, value in row.items():
                    col_xml = ET.SubElement(row_xml, 'column')
                    type_col = type(value)
                    col_xml.set('type', type_col.__name__)
                    col_xml.set('key', key)
                    if isinstance(value, bytes):
                        # convert the bytes in a hexadecimal string
                        col_xml.set('value', value.hex())
                    else:
                        # using the control char removal function to avoid xml parsing errors
                        col_xml.set('value', remove_control_chars(str(value)))

        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ", level=0)
        tree.write(dest_file, encoding='utf-8', xml_declaration=True)

