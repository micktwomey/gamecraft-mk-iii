import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamecraft.settings_heroku")

from django.core.wsgi import get_wsgi_application
from gamecraft.dj_static import Cling

application = Cling(get_wsgi_application())
