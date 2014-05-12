import os

import yaml

from gamecraft.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gamecraft',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': os.environ.get("POSTGRESQL_PORT_5432_TCP_ADDR", "localhost"),
        'PORT': os.environ.get("POSTGRESQL_PORT_5432_TCP_PORT", "5432"),
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/gamecraft/logs/request.log',
            "formatter": "request_formatter",
            'utc': True,
        },
    },
    'formatters': {
        "request_formatter": {
            "datefmt": '%Y-%m-%dT%H:%M:%S%z',
            "format": "%(asctime)s %(levelname)s %(process)d:%(thread)d %(filename)s:%(lineno)d:%(funcName)s %(message)s",
        }
    },
    'loggers': {
        '': {
            'handlers': ['request_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MEDIA_ROOT = "/gamecraft/uploads"
MEDIA_URL = "/media/"

STATIC_ROOT = "/gamecraft/static"

# Merge in /gamecraft/config/django.yaml if it exists
try:
    with open("/gamecraft/config/django.yaml") as fp:
        globals().update(**yaml.load(fp))
except FileNotFoundError:
    pass
