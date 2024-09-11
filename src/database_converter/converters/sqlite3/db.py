import concurrent.futures

from database_converter.converters.db import *
from database_converter.utils.utils import dict_factory


class SQLite3DatabaseFileConverter(DatabaseFileConverter):
    """
    Class used to convert a SQLite3 database to a python dictionary.
    """
    def __init__(self, n_threads: int = 8):
        """
        Function to instantiate a SQLite3 database converter
        :param n_threads: the number of threads to use
        """
        super(SQLite3DatabaseFileConverter, self).__init__(n_threads)

    def convert(self, db_file: str) -> dict[str, any]:
        """
        Function to convert the content of a SQLite3 database into a python object using multithreading.
        :return: a representation of the database as a python dictionary
        """
        tables_content: dict[str, any] = {}
        with sqlite3.connect(db_file) as conn:
            # return the query items as dictionaries
            conn.row_factory = dict_factory
            # create a cursor
            cur = conn.cursor()

            # get the tables in the database
            db_tables_dict = cur.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()

            # get the table names as a list
            db_table_names: list[str] = [r['name'] for r in db_tables_dict]

            # extract the tables using multithreading (1 table = 1 thread)
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_threads) as executor:
                futures = {
                    executor.submit(
                        self.extract_rows,
                        db_file=db_file,
                        table_name=table_name
                    ): table_name for table_name in db_table_names
                }
                for future in concurrent.futures.as_completed(futures):
                    table_content = future.result()
                    tables_content.update(table_content)

        database_content = {
            db_file: tables_content
        }

        return database_content
