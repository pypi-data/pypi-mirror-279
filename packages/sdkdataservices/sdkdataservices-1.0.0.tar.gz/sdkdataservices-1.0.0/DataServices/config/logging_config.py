'''import logging.config
import os
from datetime import datetime

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Get current date
current_date = datetime.now().strftime('%Y-%m-%d')

# Define logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s [%(threadName)s] %(levelname)-5s %(name)s - %(message)s',
            'datefmt': '%H:%M:%S'
        },
        'file': {
            'format': '%(asctime)s %(levelname)s %(name)s [%(threadName)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'level': 'INFO',
            'filename': f'logs/app_{current_date}.log',
            'when': 'midnight',
            'backupCount': 30,
            'encoding': 'utf8'
        },
        'size_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'level': 'INFO',
            'filename': f'logs/app_{current_date}.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'main': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }
    },
    'root': {
        'handlers': ['size_file', 'console'],
        'level': 'INFO'
    }
}

'''