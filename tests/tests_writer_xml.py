import unittest
import hashlib


from database_converter.converters.sqlite3.db import SQLite3DatabaseFileConverter
import database_converter.writers.xml as xml


class TestsWriterXML(unittest.TestCase):
    def test_write(self):
        decoded_database = SQLite3DatabaseFileConverter('resources/DB2.db').convert()
        xml.write('output/xml_result.xml', decoded_database)

        # calculate the hash of the files
        with open('resources/expected_DB2_xml.xml', 'rb') as expected_file:
            expected_hash = hashlib.md5(expected_file.read()).hexdigest()
        with open('output/xml_result.xml', 'rb') as generated_file:
            generated_hash = hashlib.md5(generated_file.read()).hexdigest()

        self.assertEqual(expected_hash, generated_hash)


if __name__ == '__main__':
    unittest.main()
