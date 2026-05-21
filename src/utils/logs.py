import os
import logging
import logging.config

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")
LOG_PATH = os.path.join(STORAGE_DIR, "logs.log")

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_PATH,
            'encoding': 'utf-8',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}

if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

logging.config.dictConfig(LOGGING_CONFIG)