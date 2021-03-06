from django.conf.urls import patterns, include, url
from django.contrib import admin

import django_nav

admin.autodiscover()
django_nav.autodiscover()

urlpatterns = patterns('',
    # backend manager
    url(r'^retrv/', include('retrvhome.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^', include('dashboard.urls')),
    # admin module
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
