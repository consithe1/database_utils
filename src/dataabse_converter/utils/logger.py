import logging
from logging.handlers import RotatingFileHandler
import sys


import dataabse_converter.utils.constants as constants


log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger(constants.PACKAGE_NAME)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

logger_error = logging.getLogger(f'{constants.PACKAGE_NAME} Errors')
file_handler = RotatingFileHandler(constants.ERROR_LOG_FILE, maxBytes=20000000)
file_handler.setFormatter(log_formatter)
logger_error.addHandler(file_handler)
logger_error.setLevel(logging.ERROR)