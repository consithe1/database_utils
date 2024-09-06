import hashlib
import unittest


import database_converter.writers.json as json


class TestsWriterJson(unittest.TestCase):

    def test_write(self):
        extracted_db = {
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
        json.write('output/json_result.json', extracted_db)

        # calculate the hash of the files
        with open('output/json_result.json', 'rb') as generated_file:
            generated_hash = hashlib.md5(generated_file.read()).hexdigest()
        with open('resources/expected_json.json', 'rb') as expected_file:
            expected_hash = hashlib.md5(expected_file.read()).hexdigest()

        self.assertEqual(generated_hash, expected_hash)


if __name__ == '__main__':
    unittest.main()
