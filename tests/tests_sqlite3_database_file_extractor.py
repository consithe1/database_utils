import unittest


from dataabse_converter.extractors.sqlite3.db import SQLite3DatabaseFileExtractor


class TestSQLite3DatabaseFileExtractor(unittest.TestCase):

    def test_extract(self):
        extractor = SQLite3DatabaseFileExtractor("resources/DB1.db")
        db_content = extractor.extract()

        expected_db_content = {
            "resources/DB1.db": {
                "Tab1": [
                    {"userId": "XB4F", "convId": "av7-dp", "sent": 1},
                    {"userId": "C2V6", "convId": None, "sent": 0},
                ],
                "Tab2": [
                    {"convId": "uaz-57", "messageId": 1, "extKey": "chat"},
                    {"convId": "r2d-2a", "messageId": 3, "extKey": "27FwAPH4QapLXF5fhDcs7"},
                    {"convId": "av7-dp", "messageId": 5, "extKey": "vache"},
                    {"convId": "xyz-ab", "messageId": 2, "extKey": "poulet"},
                ]
            }
        }

        self.assertEqual(expected_db_content, db_content)


if __name__ == '__main__':
    unittest.main()
