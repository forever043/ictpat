from django.conf.urls import patterns, include, url

urlpatterns = patterns('scrmgr.views',
    url(r'^$', 'scrmgr'),
)

