from django.conf.urls import patterns, include, url

from gamecraft.gamecrafts import feeds

urlpatterns = patterns('gamecraft.gamecrafts',
    url(r'^$', 'views.list_gamecrafts', name='list_gamecrafts'),
    url(r'^rss/$', feeds.GameCraftRSSFeed(), name="gamecraft_rss"),
    url(r'^new/$', 'views.new_gamecraft', name='new_gamecraft'),
    url(r'^(?P<slug>[^/]+)/edit/$', 'views.edit_gamecraft', name='edit_gamecraft'),
    url(r'^(?P<slug>[^/]+)/$', 'views.view_gamecraft', name='view_gamecraft'),
    url(r'^(?P<slug>[^/]+)/background/$', 'views.view_background', name='view_gamecraft_background'),
)
