import logging
import os
from datetime import datetime



def logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Create a logger with the specified name and level.

    :param name: Name of the logger.
    :param level: Logging level (default is DEBUG).
    :return: Configured logger instance.
    """

    #datetime1 = datetime.strftime(datetime.now(), '%Y-%m-%dT%H-%M-%S')
    LOG_FILENAME = 'app.log'


    #if os.path.exists(LOG_FILENAME):
    #    os.remove(LOG_FILENAME)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger