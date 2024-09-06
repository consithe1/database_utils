import unittest


import database_converter.readers.json as json


class TestReaderJson(unittest.TestCase):
    def test_read_json(self):
        content_read = json.read('resources/expected_json.json')

        expected = {
            "resources/dummy.db": {
                "Tab1": [
                    {"userId": "C2V6", "convId": None, "sent": 0}
                ],
                "Tab2": [
                    {"convId": "uaz-57", "messageId": 1, "extKey": "chat"},
                    {"convId": "r2d-2a", "messageId": 3, "extKey": "27FwAPH4QapLXF5fhDcs7"},
                    {"convId": "av7-dp", "messageId": 5, "extKey": b'\x00\x00\x04\x0f'}
                ]
            }
        }

        self.assertEqual(expected, content_read)


if __name__ == '__main__':
    unittest.main()
