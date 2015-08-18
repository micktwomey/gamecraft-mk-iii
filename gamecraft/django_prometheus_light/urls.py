from django.conf.urls import patterns, url

from .views import metrics

urlpatterns = patterns(
    '',
    url(r'^metrics/$', metrics, name='metrics'),
)
