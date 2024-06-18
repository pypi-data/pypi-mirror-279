import logging.config  # needed when logging_config doesn't start with logging.config
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(thread)d %(module)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S.%f',
        },
        'simple': {
            'format': '%(asctime)s-%(levelname)s-%(message)s ',
            'datefmt': '%Y-%m-%d %H:%M:%S.%f',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{CURRENT_DIR}/hard_conn.log',  # log file path
            'maxBytes': 1024 * 1024 * 50,  # 50 MB
            'backupCount': 5,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'hard_conn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}


logging.config.dictConfig(DEFAULT_LOGGING)
