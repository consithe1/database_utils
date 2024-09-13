import unittest


from database_converter.utils.utils import *
import database_converter.utils.constants as constants


class TestUtils(unittest.TestCase):

    def test_check_file_type(self):
        self.assertEqual(True, check_file_type('resources/DB1.db', constants.SQLITE3_DB))
        self.assertEqual(False, check_file_type('resources/expected_DB2_xml.xml', constants.SQLITE3_WAL))
        self.assertEqual(False, check_file_type('resources/db-wal', constants.SQLITE3_WAL))

    def test_conversion_for_writing(self):
        self.assertEqual({'type': 'int', 'value': '123'}, conversion_for_writing(123))
        self.assertEqual({'type': 'float', 'value': '2.456'}, conversion_for_writing(2.456))
        self.assertEqual({'type': 'str', 'value': 'test-string'}, conversion_for_writing('test-string'))
        self.assertEqual({'type': 'bytes', 'value': '000102'}, conversion_for_writing(b'\x00\x01\x02'))
        self.assertEqual({'type': 'NoneType', 'value': 'None'}, conversion_for_writing(None))

    def test_remove_control_chars_bytes(self):
        expected = [b'1', b'test', b'^{']

        self.assertEqual(expected, remove_control_chars_and_split_bytes(b'\x001\x01\x02test\x02\x00\x00^{'))


if __name__ == '__main__':
    unittest.main()
