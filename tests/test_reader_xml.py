import unittest


from database_converter.converters.sqlite3.db import SQLite3DatabaseFileConverter
import database_converter.readers.xml as xml


class TestReaderXML(unittest.TestCase):
    def test_read(self):
        expected = SQLite3DatabaseFileConverter('resources/DB2.db').convert()

        read_from_file = xml.read('resources/expected_DB2_xml.xml')
        self.assertEqual(expected, read_from_file)


if __name__ == '__main__':
    unittest.main()
