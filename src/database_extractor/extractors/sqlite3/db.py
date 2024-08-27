import sqlite3

from database_extractor.extractors.db import DatabaseFileExtractor
from database_extractor.utils.utils import dict_factory


class SQLite3DatabaseFileExtractor(DatabaseFileExtractor):
    def __init__(self, database_file: str, n_threads: int):
        super(SQLite3DatabaseFileExtractor, self).__init__(database_file, n_threads)

    def extract(self):
        with sqlite3.connect(self.db_file) as conn:
            # return the query items as dictionaries
            conn.row_factory = dict_factory
            # create a cursor
            cur = conn.cursor()

            # get the tables in the database
            db_tables_dict = cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()

            # get the table names as a list
            db_table_names: list[str] = [r['name'] for r in db_tables_dict]

            # extract the tables
