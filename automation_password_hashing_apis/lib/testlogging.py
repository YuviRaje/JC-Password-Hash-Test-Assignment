#!/usr/bin/env python3


import logging
import logging.config


def logback_info(filename, level, stdout=False):
    format_str = '%(asctime)s %(levelname)-8s - %(message)s'
    if stdout:
        logging.basicConfig(level=level, format=format_str)
    formatter = logging.Formatter(format_str)

    file_handler = logging.handlers.RotatingFileHandler(filename, maxBytes=10485760, backupCount=5)
    file_handler.setFormatter(formatter)
    logging.getLogger('').addHandler(file_handler)
    logging.getLogger('').setLevel(level)


