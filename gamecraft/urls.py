from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic.base import TemplateView

# from manifesto.views import ManifestView

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
    # url(r'^manifest\.appcache$', ManifestView.as_view(), name="cache_manifest"),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='gamecraft/profile.html'), name="account_profile"),
    url(r'^accounts/', include('allauth.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
else:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'gamecraft.views.get_media'),
    )
