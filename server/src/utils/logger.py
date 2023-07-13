import logging
import logging.config
import os.path
import sys
from configparser import ConfigParser
from .dictionaries import LOGGERS_NAMES


def set_logger(root_path: str, config: ConfigParser):
    """
    https://sanic.dev/en/guide/best-practices/logging.html#quick-start
    https://stackoverflow.com/questions/7507825/where-is-a-complete-example-of-logging-config-dictconfig
    https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig
    """

    BOT_ROOT_FILENAME = config.get('LOGGER', 'BOT_ROOT_FILENAME')
    BOT_ACCESS_FILENAME = config.get('LOGGER', 'BOT_ACCESS_FILENAME')
    BOT_ACCESS_LEVEL = config.get('LOGGER', 'BOT_ACCESS_LEVEL')

    SANIC_FILENAME = config.get('LOGGER', 'SANIC_FILENAME')
    SANIC_LOGGER_LEVEL = config.get('LOGGER', 'SANIC_LOGGER_LEVEL')

    logger_dict_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'standard': {
                'format': '%(asctime)s - %(message)s'
            },
            "generic": {
                "format": "%(asctime)s [%(process)s] [%(levelname)s] %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            },
            "access": {
                "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
                          + "%(request)s %(message)s %(status)s %(byte)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
                "class": "logging.Formatter",
            },
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout,
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout,
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout,
            },
            "bot_root_file": {
                'class': 'logging.FileHandler',
                'filename': os.path.join(root_path, 'logs', BOT_ROOT_FILENAME),
                'formatter': 'generic',
            },
            "bot_access_file": {
                'class': 'logging.FileHandler',
                'filename': os.path.join(root_path, 'logs', BOT_ACCESS_FILENAME),
                'formatter': 'generic',
            },
            "sanic_file": {
                'class': 'logging.FileHandler',
                'filename': os.path.join(root_path, 'logs', SANIC_FILENAME),
                'formatter': 'generic',
            }
        },
        loggers={
            LOGGERS_NAMES['ROOT']: {
                'handlers': ['console', 'bot_root_file'],
                'qualname': LOGGERS_NAMES['ROOT'],
                "propagate": True,
                'level': "INFO",
            },
            LOGGERS_NAMES['ERROR']: {
                'handlers': ['error_console', 'bot_root_file'],
                "propagate": True,
                'qualname': LOGGERS_NAMES['ERROR'],
                'level': "INFO",
            },
            LOGGERS_NAMES['ACCESS']: {
                'handlers': ['access_console', 'bot_access_file'],
                'level': BOT_ACCESS_LEVEL,
                "propagate": True,
                'qualname': LOGGERS_NAMES['ACCESS']
            },
            LOGGERS_NAMES['SERVER']: {
                "level": SANIC_LOGGER_LEVEL,
                "handlers": ["console", 'sanic_file'],
                "propagate": True,
                "qualname": LOGGERS_NAMES['SERVER'],
            },
        }
    )

    logging.config.dictConfig(logger_dict_config)
