from django.conf.urls import patterns, include, url

urlpatterns = patterns('gamecraft.gamecrafts',
    url(r'^$', 'views.list_gamecrafts', name='list_gamecrafts'),
    url(r'^new/$', 'views.new_gamecraft', name='new_gamecraft'),
    url(r'^(?P<slug>[^/]+)/edit/$', 'views.edit_gamecraft', name='edit_gamecraft'),
    url(r'^(?P<slug>[^/]+)/$', 'views.view_gamecraft', name='view_gamecraft'),
)
