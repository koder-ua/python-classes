#!/usr/bin/env python
# -*- encoding:utf8 -*-
"Logging module usage example"

import sys
import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def main(argv = None):
    "main function for logging example"
    if argv is None:
        argv = sys.argv

    logger = logging.getLogger('example_logging')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('example_logging.log')
    file_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(FORMAT)

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.debug("Debug msg")
    logger.info("Info msg")
    logger.warning("Warning msg")
    logger.error("Error msg")
    logger.critical("Critical msg")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Exception")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
