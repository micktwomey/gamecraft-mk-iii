"""Development "Heroku" settings

To run with these settings generate a config you can source with bash using:

    eval $(heroku config -a gamecraft-it-staging --shell | sed -E 's/^([A-Z_]+=)(.*)/export \1"\2"/g')

For fish:

    source (heroku config -a gamecraft-it-staging --shell | sed -E 's/^([A-Z_]+)=(.*)/set -x \1 "\2"/g' | psub)

"""

from gamecraft.settings_heroku_base import *

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar.apps.DebugToolbarConfig',
)

INTERNAL_IPS = ['127.0.0.1', 'localhost', '::1']

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "gamecraft.utils.debug_toolbar_callback",
}

IMAGEKIT_CACHE_BACKEND = "mock.Mock"
