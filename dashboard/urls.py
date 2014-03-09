from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from dashboard.views import *

urlpatterns = patterns('',
    url(r'^$', login_required(DashboardView.as_view()), name='dashboard'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'}, name='dashboard-login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/dashboard/login/'}, name='dashboard-logout'),
    url(r'^patent/', include('patmgr.urls')),
    url(r'^scr/', include('scrmgr.urls')),
	url(r'^sys/', include('sysmgr.urls')),
)

