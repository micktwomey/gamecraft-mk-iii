from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'gamecraft.events.views.event_list', name='event_list'),
    url(r'^new/$', 'gamecraft.events.views.new_event', name='new_event'),
)
