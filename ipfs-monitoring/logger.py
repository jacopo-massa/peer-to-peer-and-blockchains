"""
Module to setup a logger.
"""

import logging
import sys

from utils import *

# define default formatter
formatter = logging.Formatter("%(message)s", DEFAULT_DATE_FORMAT)


def setup_logger(log_name, log_file, fmt="%(message)s", level=logging.INFO):
    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    # if the file on which the logger will write to, exists, delete it, so it will be overwritten
    """if os.path.exists(log_file):
        os.remove(log_file)"""

    # setup the FileHandler
    file_handler = logging.FileHandler(log_file, delay=True)
    file_handler.setFormatter(logging.Formatter(fmt, DEFAULT_DATE_FORMAT))
    logger.addHandler(file_handler)

    # log also on stdout
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s', DEFAULT_DATE_FORMAT))
    logger.addHandler(out_hdlr)
    return logger
