PACKAGE_NAME = "database_converter"
ERROR_LOG_FILE = f"{PACKAGE_NAME}_errors.log"

SEP_KEY_CHAR = "-"

CHAT_EQUIVALENT = {'8': {'13': 97}}

SQLITE3_DB = 'sqlite3-db'
SQLITE3_WAL = 'sqlite3-wal'

FILE_HEADERS = {
    SQLITE3_DB: (b'SQLite format 3\x00', 16),
    SQLITE3_WAL: (b'\x37\x7F\x06\x82', 4)
}
