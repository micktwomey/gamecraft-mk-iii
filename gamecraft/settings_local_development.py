from gamecraft.settings import *

import os

DJANGO_SECRET_KEY = "foo"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get("GAMECRAFT_SQLITE_DB", "/tmp/gamecraft.sqlite"),
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar.apps.DebugToolbarConfig',
)

INTERNAL_IPS = ['127.0.0.1', 'localhost', '::1']

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "gamecraft.utils.debug_toolbar_callback",
}

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
