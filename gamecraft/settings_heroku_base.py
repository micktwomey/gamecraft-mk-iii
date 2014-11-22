"""Base Heroku settings

"""
import os

import dj_database_url

import mongoengine

from gamecraft.settings import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Set up the mongo connection
mongoengine.connect("gamecraft", host=os.environ["MONGOSOUP_URL"])

MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "mongoengine.django.storage.GridFSStorage"

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'gamecraft': {
        'source_filenames': (
            'css/gamecraft.less',
            'css/leaflet.css',
        ),
        'output_filename': 'css/gamecraft.css',
    },
}

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

PIPELINE_JS = {
    'gamecraft': {
        'source_filenames': (
            'js/holder.js',
            'js/jquery.js',
            'js/bootstrap.js',
            'js/leaflet.js',
            # 'js/react-with-addons.js',  # bug in processing the '\uFEFF' in the file
        ),
        'output_filename': 'js/gamecraft.js',
    },
}

IMAGEKIT_CACHE_BACKEND = "default"
