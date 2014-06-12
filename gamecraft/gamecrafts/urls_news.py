from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gamecraft.gamecrafts.views_news',
    url(r'^$', 'news_index', name='news_index'),
    url(r'^(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/(?P<slug>[^/]+)/$', 'view_news', name='view_news'),
)
