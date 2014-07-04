"""Random utils

"""


def debug_toolbar_callback(request):
    from django.conf import settings
    return settings.DEBUG
