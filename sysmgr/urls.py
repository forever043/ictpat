from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from sysmgr.views import *

urlpatterns = patterns('',
    url(r'^$',			  RedirectView.as_view(pattern_name='sysmgr-meta'), name='sysmgr'),
    url(r'^meta/$',		  MetaMgrView.as_view(),							name='sysmgr-meta'),
)

