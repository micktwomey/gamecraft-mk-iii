from django.conf.urls import patterns, include, url
from django.contrib import admin

from manifesto.views import ManifestView

urlpatterns = patterns('',
    url(r'^$', 'gamecraft.views.frontpage', name='frontpage'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manifest\.appcache$', ManifestView.as_view(), name="cache_manifest"),
)
