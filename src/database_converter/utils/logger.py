import logging
import sys


import database_converter.utils.constants as constants


log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


logger = logging.getLogger(constants.PACKAGE_NAME)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
