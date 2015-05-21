# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView, TemplateView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from sysmgr.views import *
from dashboard.forms import ExpertProfileEditForm

urlpatterns = patterns('',
    url(r'^$',         RedirectView.as_view(pattern_name='sysmgr-meta'), name='sysmgr'),
    url(r'^meta/$',    MetaMgrView.as_view(),							name='sysmgr-meta'),
    url(r'^import/$',  TemplateView.as_view(template_name='sysmgr/import.html'), name='sysmgr-import'),
    url(r'^upload/$',  TemplateView.as_view(template_name='sysmgr/file_upload.html'), name='sysmgr-upload'),
    #url(r'^profile/$', UpdateView.as_view(template_name='sysmgr/profile.html', model=User, form_class=ExpertProfileForm), name='sysmgr-profile'),
    url(r'^profile/$',
        UserProfileUpdateView.as_view(
            template_name='sysmgr/profile.html',
            form_class=ExpertProfileEditForm,
            success_url=reverse_lazy('sysmgr-profile'),
            success_message=u'个人信息更新成功'
        ),
        name='sysmgr-profile'),
)

