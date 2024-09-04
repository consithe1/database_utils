import unittest


from database_converter.utils.utils import check_file_type
import database_converter.utils.constants as constants


class TestUtils(unittest.TestCase):

    def test_check_file_type(self):
        self.assertEqual(True, check_file_type('resources/DB1.db', constants.SQLITE3_DB))
        self.assertEqual(False, check_file_type('resources/expected_DB2_xml.xml', constants.SQLITE3_WAL))
        self.assertEqual(False, check_file_type('resources/db-wal', constants.SQLITE3_WAL))


if __name__ == '__main__':
    unittest.main()
