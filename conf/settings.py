"""
用于存放项目配置信息
"""
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

USER_DATA_DIR = os.path.join(BASE_DIR, 'db', 'user_data')

"""
logger配置
"""

standard_format = '[%(asctime)s][%(threadName)s:%(tread)d][task_id:%(name)s][%(filename)s:%(lineon)d]' \
                  '[%(levelname)s][%(message)s]'
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineon)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

logfile_dir = os.path.join(BASE_DIR, 'log')

logfile_name = 'atm.log'

if not os.path.isdir(logfile_dir):
    os.mkdir(logfile_dir)

logfile_path = os.path.join(logfile_dir, logfile_name)

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard'
            'filename': 'logfile_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
