import unittest


from database_converter.converters.sqlite3.db import SQLite3DatabaseFileConverter


class TestSQLite3DatabaseFileConverter(unittest.TestCase):

    def test_extract(self):
        extractor = SQLite3DatabaseFileConverter("resources/DB2.db")
        db_content = extractor.convert()

        expected_db_content = {'resources/DB2.db': {'Tab1': [{'userId': 'JZDT', 'username': 'John'}, {'userId': 'C2V6', 'username': 'Charles'}, {'userId': 'R7UN', 'username': 'Richard'}, {'userId': 'XB4F', 'username': 'Xavier'}], 'Tab2': [{'extKey': '27FwAPH4QapLXF5fhDcs7', 'convContent - 1': 'Aw/StKU4rGc7uQy9L1O3r0kWNoCi55HRRHwU21MCVpQ=', 'convContent - 2': '4Et6zpGgHRbzvMzQLB7MIQ==', 'convContent - 3': 1, 'convContent - 6 - 1': 'https://cf-st.sc-cdn.net/f/27FwAPH4QapLXF5fhDcs7', 'convContent - 6 - 4': '1:3268ee78-5bea-53d2-b12c-d362df90dffb:93917:0:0', 'convContent - 6 - 7 - 1': 'uc', 'convContent - 6 - 7 - 2': '4', 'convContent - 6 - 15 - 1': '1:3268ee78-5bea-53d2-b12c-d362df90dffb:93917:0:0', 'convContent - 6 - 15 - 2': 'Chat', 'convContent - 6 - 15 - 3': 'Image', 'convContent - 7 - 1 - 2 - 2': '27FwAPH4QapLXF5fhDcs7', 'convContent - 7 - 1 - 2 - 6': b'\x06', 'convContent - 7 - 1 - 2 - 9': 2, 'convContent - 7 - 1 - 2 - 10': 4, 'convContent - 7 - 1 - 2 - 12': 1, 'convContent - 8': '27FwAPH4QapLXF5fhDcs7', 'convContent - 10': 1683893510461, 'convContent - 13': 2, 'read': 1, 'col4': 0}]}}

        self.assertEqual(expected_db_content, db_content)


if __name__ == '__main__':
    unittest.main()
