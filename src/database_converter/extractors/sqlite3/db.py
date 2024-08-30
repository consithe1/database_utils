import concurrent.futures

from database_converter.extractors.db import *
from database_converter.utils.utils import dict_factory


class SQLite3DatabaseFileExtractor(DatabaseFileExtractor):
    def __init__(self, database_file: str, n_threads: int = 8):
        super(SQLite3DatabaseFileExtractor, self).__init__(database_file, n_threads)

    def extract(self):
        tables_content: dict[str, any] = {}
        with sqlite3.connect(self.db_file) as conn:
            # return the query items as dictionaries
            conn.row_factory = dict_factory
            # create a cursor
            cur = conn.cursor()

            # get the tables in the database
            db_tables_dict = cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()

            # get the table names as a list
            db_table_names: list[str] = [r['name'] for r in db_tables_dict]

            # extract the tables using multiprocessing
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_threads) as executor:
                futures = {
                    executor.submit(
                        self.extract_rows,
                        table_name=table_name
                    ): table_name for table_name in db_table_names
                }
                for future in concurrent.futures.as_completed(futures):
                    table_content = future.result()
                    tables_content.update(table_content)

        database_content = {
            self.db_file: tables_content
        }

        return database_content
