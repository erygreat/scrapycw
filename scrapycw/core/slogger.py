import logging
import os
from scrapycw.settings import LOGGERG_LEVEL, LOGGING_FILE

def get_filename():
    filename = LOGGING_FILE
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return filename


def add_handler(logger, level):
    filename = get_filename()
    level = level if level else LOGGERG_LEVEL
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

def getLogger(name = 'default', level = None):
    logger = logging.getLogger(name);
    if not logger.handlers:
        add_handler(logger, level)
    return logger

