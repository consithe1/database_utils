

class DatabaseFileExtractor:
    def __init__(self, filepath: str, n_threads: int = 8):
        self.db_file: str = filepath
        self.n_threads: int = n_threads
