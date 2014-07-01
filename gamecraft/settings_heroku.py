import os
import urllib.parse

import dj_database_url

from gamecraft.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

redis_parse_result = urllib.parse.urlparse(os.environ['REDISCLOUD_URL'])
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '{redis.hostname}:{redis.port}:0'.format(redis=redis_parse_result),
        'OPTIONS': {
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
            'PASSWORD': redis_parse_result.password,
            'PICKLE_VERSION': -1,
            'IGNORE_EXCEPTIONS': True,
            'CONNECTION_POOL_KWARGS': {'max_connections': 10}
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

SESSION_CACHE_ALIAS = 'default'
