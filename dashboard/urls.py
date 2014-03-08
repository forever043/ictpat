from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', 'dashboard.views.dashboard', name='dashboard'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'}, name='dashboard-login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/dashboard/login/'}, name='dashboard-logout'),
    url(r'^patent/', include('patmgr.urls')),
    url(r'^scr/', include('scrmgr.urls')),
	url(r'^sys/', include('sysmgr.urls')),
)

