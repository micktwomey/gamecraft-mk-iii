from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic.base import TemplateView

# from manifesto.views import ManifestView


def robots_txt(request):
    return HttpResponse("User-agent: *\nDisallow:", content_type="text/plain")

urlpatterns = patterns('',
    url(r'^$', 'gamecraft.views.frontpage', name='frontpage'),
    url(r"^codeofconduct/$", 'gamecraft.views.codeofconduct', name='codeofconduct'),
    url(r"^colophon/$", 'gamecraft.views.colophon', name='colophon'),
    url(r"^privacy/$", 'gamecraft.views.privacy', name='privacy'),
    url(r"^legal/$", 'gamecraft.views.legal', name='legal'),
    url(r"^thanks/$", 'gamecraft.views.thanks', name='thanks'),
    url(r'^events/', include('gamecraft.gamecrafts.urls')),
    url(r'^news/', include('gamecraft.gamecrafts.urls_news')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'gamecraft.views.get_media'),
    url(r'^robots.txt$', robots_txt),
)
