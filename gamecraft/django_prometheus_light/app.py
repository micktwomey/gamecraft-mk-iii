from django.apps import AppConfig
from django.conf import settings

from prometheus_client import start_http_server


class DjangoPrometheusLightAppConfig(AppConfig):
    name = 'gamecraft.django_prometheus_light'
    verbose_name = "Django Prometheus Light"

    def ready(self):
        # Import the signals to register them
        from . import signals
