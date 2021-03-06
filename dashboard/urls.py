# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from dashboard.views import *
from dashboard.models import ExpertProfile


urlpatterns = patterns('',
                       url(r'^$', login_required(DashboardView.as_view()), name='dashboard'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'dashboard/login.html'},
                           name='dashboard-login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/dashboard/login/'},
                           name='dashboard-logout'),
                       url(r'^patent/', include('patmgr.urls')),
                       url(r'^scr/', include('scrmgr.urls')),
                       url(r'^rank/', include('rankmgr.urls')),

                       url(r'^sys/', include('sysmgr.urls')),

                       url(r'^user/data/$',
                           login_required(DashMgrListJson.as_view(
                               model=User,
                               retrieve_list=[],
                               columns=['name', 'email', 'department'],
                               column_template={
                                   "name": lambda o: u'%s%s' % (o.last_name, o.first_name),
                                   "email": lambda o: u'%s' % o.email,
                                   "department": lambda o: u'%s' % '----',
                               })),
                           name='user-list-json'),

                       url(r'^expert/list/data/$',
                           login_required(ExpertListJson.as_view(
                               model=User,
                               columns=['name', 'email', 'research', 'department'],
                               column_template={
                                   "name": lambda o: u'%s%s' % (o.last_name, o.first_name),
                                   "email": lambda o: u'%s' % o.email,
                                   "research": lambda o: u'%s' % o.expertprofile.research_field,
                                   "department": lambda o: u'%s' % o.expertprofile.organization,
                               })),
                           name='expert-list-json'),
)

