from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


@never_cache
def metrics(request):
    """Exposes prometheus metrics"""
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)
